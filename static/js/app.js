/*global Vue, todoStorage */

(function (exports) {

    'use strict';

    const URL = '/todo';

    exports.app = new Vue({

        // the root element that will be compiled
        el: '.todoapp',

        // app initial state
        data: {
            todos: [],
            task: '',
            todo: '',
            editedTodo: null,
            visibility: 'all'
        },

        // methods that implement data logic.
        // note there's no DOM manipulation here at all.
        methods: {

            getTodos: function () {
                axios.get(URL)
                    .then(response => {
                        // JSON responses are automatically parsed.
                        console.log(response.data);
                        this.todos = response.data;
                    })
                    .catch(e => {
                        console.error(e);
                        return [];
                    });
            },

            addTodo: function () {
                let value = this.task && this.task.trim();
                if (!value) {
                    return;
                }
                axios.post(URL, {
                    "todo": {
                        "task": this.task
                    }
                }).then(response => {
                    // JSON responses are automatically parsed.
                    console.log(response.data);
                    this.getTodos();
                }).catch(e => {
                    console.error(e)
                });
                this.task = '';
            },

            removeTodo: function (todo) {
                console.log("deleting " + todo.todo_id);
                axios.delete(URL + "?todo_id=" + todo.todo_id
                ).then(response => {
                    // JSON responses are automatically parsed.
                    this.getTodos();
                }).catch(e => {
                    console.error(e);
                    return [];
                });
            }
        },

        // a custom directive to wait for the DOM to be updated
        // before focusing on the input field.
        // http://vuejs.org/guide/custom-directive.html
        directives: {
            'todo-focus': function (el, binding) {
                if (binding.value) {
                    el.focus();
                }
            }
        },
        mounted: function () {
            this.getTodos();
        }


    });

})(window);