from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)
user_tokens = []


def _create_users():
    for i in range(10):
        response = client.post(
            "/user/create",
            json={"user_name": f"room_user_{i}", "leader_card_id": 1000},
        )
        user_tokens.append(response.json()["user_token"])


_create_users()


def _auth_header(i=0):
    token = user_tokens[i]
    return {"Authorization": f"bearer {token}"}


def test_room_1():
    response = client.post(
        "/room/create",
        headers=_auth_header(),
        json={"live_id": 1001, "select_difficulty": 1},
    )
    assert response.status_code == 200

    room_id = response.json()["room_id"]
    print(f"room/create {room_id=}")

    response = client.post("/room/list", json={"live_id": 1001})
    assert response.status_code == 200
    print("room/list response:", response.json())

    response = client.post(
        "/room/wait", headers=_auth_header(), json={"room_id": room_id}
    )
    assert response.status_code == 200
    print("room/wait response:", response.json())

    response = client.post(
        "/room/start", headers=_auth_header(), json={"room_id": room_id}
    )
    assert response.status_code == 200
    print("room/wait response:", response.json())

    response = client.post(
        "/room/end",
        headers=_auth_header(),
        json={
            "room_id": room_id,
            "score": 1234,
            "judge_count_list": [1111, 222, 33, 44, 5],
        },
    )
    assert response.status_code == 200
    print("room/end response:", response.json())

    response = client.post(
        "/room/result",
        json={"room_id": room_id},
    )
    assert response.status_code == 200
    print("room/result response:", response.json())


def test_room_2():
    response = client.post(
        "/room/create",
        headers=_auth_header(),
        json={"live_id": 1002, "select_difficulty": 1},
    )
    assert response.status_code == 200

    room_id = response.json()["room_id"]
    print(f"room/create {room_id=}")

    for i in range(5):
        response = client.post(
            "/room/join",
            headers=_auth_header(i),
            json={"room_id": room_id, "select_difficulty": 1},
        )
        print(response.text)
        assert response.status_code == 200
        if i == 0:
            assert response.json()["join_room_result"] == 4
        elif i == 4:
            assert response.json()["join_room_result"] == 2
        else:
            assert response.json()["join_room_result"] == 1

    response = client.post(
        "/room/start", headers=_auth_header(), json={"room_id": room_id}
    )
    assert response.status_code == 200

    response = client.post(
        "/room/leave",
        headers=_auth_header(0),
        json={"room_id": room_id},
    )
    assert response.status_code == 200

    response = client.post(
        "/room/leave",
        headers=_auth_header(1),
        json={"room_id": room_id},
    )
    assert response.status_code == 200

    response = client.post(
        "/room/join",
        headers=_auth_header(0),
        json={"room_id": room_id, "select_difficulty": 1},
    )
    assert response.status_code == 200

    response = client.post(
        "/room/leave",
        headers=_auth_header(2),
        json={"room_id": room_id},
    )
    assert response.status_code == 200
    print(response.json())

    response = client.post(
        "/room/leave",
        headers=_auth_header(3),
        json={"room_id": room_id},
    )
    assert response.status_code == 200
    print(response.json())

    response = client.post(
        "/room/leave",
        headers=_auth_header(0),
        json={"room_id": room_id},
    )
    assert response.status_code == 200
    print(response.json())

    response = client.post(
        "/room/join",
        headers=_auth_header(0),
        json={"room_id": room_id, "select_difficulty": 1},
    )
    assert response.status_code == 200
    print(room_id)
    print(response.text)
