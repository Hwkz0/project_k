"""Tests for quest endpoints."""

import pytest
from fastapi import status


class TestQuestEndpoints:
    """Test quest endpoints."""

    @pytest.fixture
    def test_quest(self, db):
        """Create a test quest."""
        from app.models.quest import Quest, QuestDifficulty, QuestCategory
        
        quest = Quest(
            title="Test Quest",
            description="Complete this quest for testing",
            difficulty=QuestDifficulty.EASY,
            category=QuestCategory.DEVELOPMENT,
            xp_reward=25,
            is_active=True,
            is_repeatable=False,
        )
        db.add(quest)
        db.commit()
        db.refresh(quest)
        return quest

    def test_list_quests(self, client, test_quest):
        """Test listing quests."""
        response = client.get("/api/v1/quests/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert any(q["title"] == "Test Quest" for q in data)

    def test_get_quest(self, client, test_quest):
        """Test getting a specific quest."""
        response = client.get(f"/api/v1/quests/{test_quest.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Test Quest"
        assert data["xp_reward"] == 25

    def test_get_nonexistent_quest(self, client):
        """Test getting non-existent quest fails."""
        response = client.get("/api/v1/quests/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_complete_quest(self, client, auth_headers, test_quest, test_user, db):
        """Test completing a quest."""
        response = client.post(
            f"/api/v1/quests/{test_quest.id}/complete",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quest_id"] == test_quest.id
        assert data["xp_earned"] == 25

        # Verify user XP was updated
        db.refresh(test_user)
        assert test_user.xp == 25

    def test_complete_quest_twice(self, client, auth_headers, test_quest):
        """Test completing non-repeatable quest twice fails."""
        # Complete first time
        response1 = client.post(
            f"/api/v1/quests/{test_quest.id}/complete",
            headers=auth_headers,
        )
        assert response1.status_code == status.HTTP_200_OK

        # Try to complete again
        response2 = client.post(
            f"/api/v1/quests/{test_quest.id}/complete",
            headers=auth_headers,
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_quest_status(self, client, auth_headers, test_quest):
        """Test getting quest completion status."""
        # Before completion
        response1 = client.get(
            f"/api/v1/quests/{test_quest.id}/status",
            headers=auth_headers,
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json()["is_completed"] == False
        assert response1.json()["can_complete"] == True

        # Complete the quest
        client.post(
            f"/api/v1/quests/{test_quest.id}/complete",
            headers=auth_headers,
        )

        # After completion
        response2 = client.get(
            f"/api/v1/quests/{test_quest.id}/status",
            headers=auth_headers,
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()["is_completed"] == True
        assert response2.json()["can_complete"] == False

    def test_create_quest(self, client, auth_headers):
        """Test creating a quest."""
        response = client.post(
            "/api/v1/quests/",
            headers=auth_headers,
            json={
                "title": "New Quest",
                "description": "A brand new quest",
                "difficulty": "medium",
                "category": "testing",
                "xp_reward": 50,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "New Quest"
        assert data["xp_reward"] == 50
