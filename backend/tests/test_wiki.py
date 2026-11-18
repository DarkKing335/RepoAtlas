"""Unit tests for the Wiki Generation engine (Epic 4)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from wiki_generation.renderer import (
    WIKI_OUTPUT_DIR,
    generate_search_index,
    render_html_page,
    render_index_page,
    render_symbol_pages,
    generate_ai_context,
)


def test_render_html_page():
    section_data = {
        "title": "Technology Stack Test",
        "body": "Test body description.",
        "facts": {
            "languages": ["java", "csharp"],
            "frameworks": ["Spring Boot"],
        },
    }
    render_html_page("tech.html", section_data)
    output_file = WIKI_OUTPUT_DIR / "tech.html"

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Technology Stack Test" in content
    assert "Test body description." in content
    assert "Spring Boot" in content


def test_render_index_page(sample_index):
    repo_dict = sample_index.model_dump()
    render_index_page(repo_dict)
    output_file = WIKI_OUTPUT_DIR / "index.html"

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "sample_repo" in content
    assert "Technology Stack" in content
    assert "Dashboard" in content


def test_render_symbol_pages(sample_index):
    repo_dict = sample_index.model_dump()
    render_symbol_pages(repo_dict)

    symbols_dir = WIKI_OUTPUT_DIR / "symbols"
    assert symbols_dir.exists()
    html_files = list(symbols_dir.glob("*.html"))
    assert len(html_files) > 0

    first_file = html_files[0]
    content = first_file.read_text(encoding="utf-8")
    assert "Source Location" in content


def test_generate_search_index(sample_index):
    repo_dict = sample_index.model_dump()
    generate_search_index(repo_dict)

    index_file = WIKI_OUTPUT_DIR / "search_index.json"
    assert index_file.exists()

    data = json.loads(index_file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    urls = [item["url"] for item in data]
    assert "index.html" in urls
    assert "tech.html" in urls
    assert "architecture.html" in urls
    assert "modules.html" in urls
    assert "tests.html" in urls
    assert any(url.startswith("symbols/") for url in urls)


def test_generate_ai_context(sample_index):
    repo_dict = sample_index.model_dump()
    analysis_data = {
        "content": [
            {"key": "tech", "title": "Technology Stack", "body": "Written in Java.", "facts": {"languages": ["java"]}},
        ],
        "summaries": [
            {"node_id": "sample_repo", "name": "sample_repo", "tier": 1, "summary": "Multi-module project."},
        ],
    }
    generate_ai_context(repo_dict, analysis_data)

    context_file = WIKI_OUTPUT_DIR / "wiki_context.json"
    assert context_file.exists()

    data = json.loads(context_file.read_text(encoding="utf-8"))
    assert "repository_name" in data
    assert "symbols" in data
    assert "sections" in data
    assert "summaries" in data

    assert len(data["symbols"]) > 0
    symbol = data["symbols"][0]
    assert "fully_qualified_name" in symbol
    assert "file_path" in symbol
    assert "url" in symbol

    assert data["sections"][0]["key"] == "tech"
    assert data["summaries"][0]["node_id"] == "sample_repo"
