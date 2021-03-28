
<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>ToDo</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todo-modal>Add ToDo</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">ToDo?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(todo, index) in todos" :key="index">
              <td>{{ todo.title }}</td>
              <td>{{ todo.desc }}</td>
              <td>
                <span v-if="todo.done">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-outline-warning btn-sm"
                          v-b-modal.todo-update-modal
                          @click="editToDo(todo)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-outline-danger btn-sm"
                          @click="onDeleteToDo(todo)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addToDoModal"
            id="todo-modal"
            title="Add a new ToDo"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addToDoForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-desc-group"
                      label="Desc:"
                      label-for="form-descr-input">
            <b-form-input id="form-desc-input"
                          type="text"
                          v-model="addToDoForm.desc"
                          required
                          placeholder="Enter desc">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-done-group">
          <b-form-checkbox-group v-model="addToDoForm.done" id="form-checks">
            <b-form-checkbox value="true">Done?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="outline-primary">Submit</b-button>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editToDoModal"
            id="todo-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-desc-edit-group"
                      label="Desc:"
                      label-for="form-desc-edit-input">
            <b-form-input id="form-desc-edit-input"
                          type="text"
                          v-model="editForm.desc"
                          required
                          placeholder="Enter desc">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-done-edit-group">
          <b-form-checkbox-group v-model="editForm.done" id="form-checks">
            <b-form-checkbox value="true">Done?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';
export default {
  data() {
    return {
      todos: [],
      addToDoForm: {
        title: '',
        desc: '',
        done: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        title: '',
        desc: '',
        done: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getToDos() {
      const path = 'http://localhost:5000/todos';
      axios.get(path)
        .then((res) => {
          this.todos = res.data.todos;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addToDo(payload) {
      const path = 'http://localhost:5000/todos';
      axios.post(path, payload)
        .then(() => {
          this.getToDos();
          this.message = 'ToDo added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getToDos();
        });
    },
    initForm() {
      this.addToDoForm.title = '';
      this.addToDoForm.desc = '';
      this.addToDoForm.done = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.desc = '';
      this.editForm.done = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addToDoModal.hide();
      let done = false;
      if (this.addToDoForm.done[0]) done = true;
      const payload = {
        title: this.addToDoForm.title,
        desc: this.addToDoForm.desc,
        done, // property shorthand
      };
      this.addToDo(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addToDoModal.hide();
      this.initForm();
    },
    editToDo(todo) {
      this.editForm = todo;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editToDoModal.hide();
      let done = false;
      if (this.editForm.done[0]) done = true;
      const payload = {
        title: this.editForm.title,
        desc: this.editForm.desc,
        done,
      };
      this.updateToDo(payload, this.editForm.id);
    },
    updateToDo(payload, todoID) {
      const path = `http://localhost:5000/todos/${todoID}`;
      axios.put(path, payload)
        .then(() => {
          this.getToDos();
          this.message = 'ToDo updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getToDos();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editToDoModal.hide();
      this.initForm();
      this.getToDos(); // why?
    },
    removeToDo(todoID) {
      const path = `http://localhost:5000/todos/${todoID}`;
      axios.delete(path)
        .then(() => {
          this.getToDos();
          this.message = 'ToDo removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getToDos();
        });
    },
    onDeleteToDo(todo) {
      this.removeToDo(todo.id);
    },
  },
  created() {
    this.getToDos();
  },
};
</script>
