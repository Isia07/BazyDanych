#!/bin/bash

API_URL="http://localhost:8000/api/v1/obj"
EMAIL="testuser_$(date +%s)@example.com"
PASSWORD="password123"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}starting ZODB API Test${NC}"
echo "target: $API_URL"

extract_id() {
    echo $1 | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))"
}
extract_token() {
    echo $1 | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))"
}

echo -e "\n${GREEN}[1] registering user...${NC}"
REQ_DATA="{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"name\": \"Test\", \"surname\": \"User\"}"
echo "request: $REQ_DATA"
REGISTER_RES=$(curl -s -X POST "$API_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $REGISTER_RES"
TOKEN=$(extract_token "$REGISTER_RES")
USER_ID=$(echo $REGISTER_RES | python3 -c "import sys, json; print(json.load(sys.stdin).get('user', {}).get('id', ''))")

if [ -z "$TOKEN" ] || [ "$TOKEN" == "None" ]; then
    echo "login to get token (if register failed/user exists)..."
    REQ_DATA="{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}"
    echo "request: $REQ_DATA"
    LOGIN_RES=$(curl -s -X POST "$API_URL/auth/login/" \
      -H "Content-Type: application/json" \
      -d "$REQ_DATA")
    TOKEN=$(extract_token "$LOGIN_RES")
fi

echo "token: $TOKEN"
AUTH_HEADER="Authorization: Token $TOKEN"

echo -e "\n${GREEN}[2] creating status...${NC}"
REQ_DATA='{"name": "active"}'
echo "request: $REQ_DATA"
STATUS_RES=$(curl -s -X POST "$API_URL/statuses/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $STATUS_RES"
STATUS_ID=$(extract_id "$STATUS_RES")

echo -e "\n${GREEN}[3] updating status...${NC}"
REQ_DATA='{"name": "very active"}'
echo "request: $REQ_DATA"
UPDATE_STATUS_RES=$(curl -s -X PATCH "$API_URL/statuses/$STATUS_ID/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $UPDATE_STATUS_RES"

echo -e "\n${GREEN}[4] creating event type...${NC}"
REQ_DATA='{"name": "concert"}'
echo "request: $REQ_DATA"
ET_RES=$(curl -s -X POST "$API_URL/event-types/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $ET_RES"
ET_ID=$(extract_id "$ET_RES")

echo -e "\n${GREEN}[5] creating event...${NC}"
EVENT_DATA=$(cat <<EOF
{
  "name": "zodb sausage fest christmas 2026",
  "description": "test event",
  "localization": "warsaw",
  "date_start": "2026-12-25T18:00:00",
  "date_end": "2026-12-25T23:00:00",
  "base_price": "44.00",
  "quantity": 128,
  "event_type_id": "$ET_ID",
  "status_id": "$STATUS_ID"
}
EOF
)
echo "request: $EVENT_DATA"
EVENT_RES=$(curl -s -X POST "$API_URL/events/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$EVENT_DATA")
echo "response: $EVENT_RES"
EVENT_ID=$(extract_id "$EVENT_RES")

echo -e "\n${GREEN}[6] updating event (PATCH)...${NC}"
REQ_DATA='{"name": "zodb sausage fest 2026"}'
echo "request: $REQ_DATA"
PATCH_EVENT_RES=$(curl -s -X PATCH "$API_URL/events/$EVENT_ID/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $PATCH_EVENT_RES"

echo -e "\n${GREEN}[7] creating ticket type...${NC}"
REQ_DATA='{"name": "ticket", "discount": "0.05"}'
echo "request: $REQ_DATA"
TT_RES=$(curl -s -X POST "$API_URL/ticket-types/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $TT_RES"
TT_ID=$(extract_id "$TT_RES")

echo -e "\n${GREEN}[8] creating discount...${NC}"
REQ_DATA='{"name": "summer sale", "discount_percentage": "0.10", "code": "SUMMER10", "valid_from": "2025-06-01T00:00:00", "valid_to": "2025-06-30T23:59:59"}'
echo "request: $REQ_DATA"
DISC_RES=$(curl -s -X POST "$API_URL/discounts/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $DISC_RES"
DISC_ID=$(extract_id "$DISC_RES")

echo -e "\n${GREEN}[9] creating order...${NC}"
ORDER_DATA=$(cat <<EOF
{
  "tickets_data": [
    {"event_id": "$EVENT_ID", "ticket_type_id": "$TT_ID", "quantity": 2}
  ],
  "discount_id": "$DISC_ID"
}
EOF
)
echo "request: $ORDER_DATA"
ORDER_RES=$(curl -s -X POST "$API_URL/orders/create/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$ORDER_DATA")
echo "response: $ORDER_RES"

echo -e "\n${GREEN}[10] listing user orders...${NC}"
echo "request: GET $API_URL/orders/"
ORDERS_LIST=$(curl -s -X GET "$API_URL/orders/" \
  -H "$AUTH_HEADER")
echo "response: $ORDERS_LIST"

echo -e "\n${GREEN}[11] sending message...${NC}"
REQ_DATA='{"text": "helo im under the water pls help me"}'
echo "request: $REQ_DATA"
MSG_RES=$(curl -s -X POST "$API_URL/messages/" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$REQ_DATA")
echo "response: $MSG_RES"

echo -e "\n${CYAN}test complete${NC}"
