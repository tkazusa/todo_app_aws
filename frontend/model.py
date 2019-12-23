# -*- coding: utf-8 -*-
from const import BASE_URL

__pragma__('alias', 'S', '$')


class Model:
    def __init__(self):
        self._todos = []

    def get_todo(self, todo_id):
        for todo in self._todos:
            if todo['id'] == todo_id:
                return todo
        return None

    def get_all_todos(self):
        return self._todos

    def load_all_todos(self):
        S.ajax({
            'url': f"{BASE_URL}todos",
            'type': 'GET',
        }).done(
            self._success_load_all_todos
        ).fail(
            lambda d: alert('サーバーとの通信に失敗しました。')
        )

    def _success_load_all_todos(self, data):
        self._todos = data
        S('body').trigger('todos-updated')

    def create_todo(self, data):
        S.ajax({
            'url': f"{BASE_URL}todos",
            'type': 'POST',
            'contentType': 'application/json',
            'data': JSON.stringify(data),
        }).done(
            self._success_create_todo
        ).fail(
            lambda d: alert('サーバーとの通信に失敗しました。')
        )

    def _success_create_todo(self, data):
        self._todos.append(data)
        S('body').trigger('todos-updated')

    def update_todo(self, todo_id, data):
        send_data = {}
        for key in ['title', 'memo', 'priority', 'completed']:
            if key in data:
                send_data[key] = data[key]
        S.ajax({
            'url': f"{BASE_URL}todos/{todo_id}",
            'type': 'PUT',
            'contentType': 'application/json',
            'data': JSON.stringify(send_data),
        }).done(
            self._success_update_todo
        ).fail(
            lambda d: alert('サーバーとの通信に失敗しました。')
        )

    def _success_update_todo(self, data):
        for i, todo in enumerate(self._todos):
            if todo['id'] == data['id']:
                self._todos[i] = data
        S('body').trigger('todos-updated')

    def toggle_todo(self, todo_id):
        todo = self.get_todo(todo_id)
        self.update_todo(todo_id, {'completed': not todo['completed']})

    def delete_todo(self, todo_id):
        S.ajax({
            'url': f"{BASE_URL}todos/{todo_id}",
            'type': 'DELETE',
        }).done(
            self._success_delete_todo
        ).fail(
            lambda d: alert('サーバーとの通信に失敗しました。')
        )

    def _success_delete_todo(self, data):
        for i, todo in enumerate(self._todos):
            if todo['id'] == data['id']:
                self._todos.pop(i)
                break
        S('body').trigger('todos-updated')
