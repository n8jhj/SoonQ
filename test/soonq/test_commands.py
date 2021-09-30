"""Tests for the commands module."""

import datetime as dt
import uuid

import pytest

from soonq.commands.commands import QueueItem


@pytest.fixture
def queue_item():
    return QueueItem(
        "994a92b2-5e74-4ddd-9208-ff185f8f133f",
        "CustomTask",
        "3",
        "2021-09-29 11:13:57.223584",
        b'\x80\x03).',  # An empty tuple.
        b'\x80\x03}q\x00.',  # An empty dict.
    )


def test_queueitem_init(queue_item):
    assert isinstance(queue_item.task_id, uuid.UUID)
    assert queue_item.queue_name == "CustomTask"
    assert isinstance(queue_item.position, int) and queue_item.position == 3
    assert isinstance(queue_item.published, dt.datetime) and queue_item.published == dt.datetime(2021, 9, 29, 11, 13, 57, 223584)
    assert isinstance(queue_item.args, tuple) and queue_item.args == ()
    assert isinstance(queue_item.kwargs, dict) and queue_item.kwargs == {}


def test_queueitem_list_item_info(queue_item):
    assert queue_item.list_item_info(truncate=True) == [
        "994a92b2-", "CustomTask", "3", "2021-09-29 11:13:57", "()", "{}",
    ]
