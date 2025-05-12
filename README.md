# connect_four

Set up the virtual env and install the dependencies with the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pipenv install
```

You'll also need to set an env var in your terminal to point the app to port 8080:

```bash
export FLASK_RUN_PORT=8080
```

Run the app with the following command:

```bash
flask --app app run
```

Then you can open a terminal and execute the follow cURL command:

```bash
curl -X POST http://localhost:8080/evaluate_board_state \
  -H "Content-Type: application/json" \
  -d '{
    "board": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 1, 1, 0],
        [0, 0, 0, 1, 1, 2, 0]
    ]
}'
```

For this particular input, you should see a response like: `{"player_next_turn":"Red","status":"in_progress"}`.
