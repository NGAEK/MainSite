from api.routes import _collect_main_metrics


def test_collect_main_metrics_shape(monkeypatch):
    monkeypatch.setattr("api.routes.get_table_names", lambda: ["admin_users", "news"])
    monkeypatch.setattr("api.routes.is_db_alive", lambda: True)
    monkeypatch.setattr("api.routes.news_repository.count_news", lambda: 2)
    monkeypatch.setattr("api.routes.admin_users_repository.count_admin_users", lambda active_only=False: 1 if active_only else 2)

    data = _collect_main_metrics()
    assert data["db_alive"] is True
    assert data["db_table_count"] == 2
    assert data["news_total"] == 2
    assert data["admin_users_total"] == 2
    assert data["admin_users_active"] == 1
    assert isinstance(data["api_uptime_seconds"], int)
    assert "generated_at" in data
