<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import Modal from "@/components/Modal.vue";

const inputFocused = ref(false);
const comments = ref([]);
const newComment = ref("");
const showModal = ref(false);
const modalMessage = ref("");
const currentUser = ref(null);

const route = useRoute();
const recipeId = parseInt(route.params.id, 10);

const fetchComments = async () => {
  try {
    const response = await axios.get("http://localhost:8000/comments/");
    comments.value = response.data.filter((comment) => comment.recipe === recipeId);
  } catch (error) {
    console.error("Ошибка загрузки комментариев:", error);
  }
};

const addComment = async () => {
  try {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      showModalMessage("Вы должны быть авторизованы для добавления комментариев.");
      return;
    }

    if (!newComment.value.trim()) {
      showModalMessage("Комментарий не может быть пустым.");
      return;
    }

    await axios.post(
      "http://localhost:8000/comments/",
      {
        recipe: recipeId,
        content: newComment.value.trim(),
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    newComment.value = "";
    fetchComments();
    showModalMessage("Комментарий успешно добавлен.");
  } catch (error) {
    console.error("Ошибка добавления комментария:", error);
  }
};

const deleteComment = async (commentId) => {
  try {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      showModalMessage("Вы должны быть авторизованы для удаления комментариев.");
      return;
    }

    await axios.delete(`http://localhost:8000/comments/${commentId}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchComments();
    showModalMessage("Комментарий успешно удалён.");
  } catch (error) {
    console.error("Ошибка удаления комментария:", error);
  }
};

const showModalMessage = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

onMounted(async() => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    try {
      const response = await axios.get("http://localhost:8000/auth/users/me/", {
        headers: { Authorization: `Token ${token}` },
      });
      currentUser.value = response.data.username;
    } catch (error) {
      console.error("Ошибка при получении имени пользователя:", error);
    }
  }
  fetchComments();
});
</script>

<template>
  <div>
    <h3>Комментарии</h3>

    <div v-if="comments.length">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item"
      >
        <p><strong>{{ comment.user }}:</strong> {{ comment.content }}</p>
        <button
          v-if="comment.user === currentUser"
          class="btn btn-danger"
          @click="deleteComment(comment.id)"
        >
          Удалить
        </button>
      </div>
    </div>
    <div v-else>
      <p>Комментариев пока нет. Будьте первым!</p>
    </div>

    <h3>Добавить комментарий</h3>
    <textarea
      v-model="newComment"
      placeholder="Напишите свой комментарий"
      class="comment-input"
      :class="{'input-focus': inputFocused}"
      @focus="inputFocused = true"
      @blur="inputFocused = false"
    ></textarea>
    <button @click="addComment" class="save-button">
      Добавить
    </button>

    <Modal
      :isVisible="showModal"
      :message="modalMessage"
      @close="showModal = false"
    />
  </div>
</template>

<style scoped>
.comment-item {
  background-color: var(--comment-bg-color);
  border: 1px solid #D5B69D;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.comment-input {
  background-color: var(--input-bg-color);
  color: var(--text-color);
  width: 100%;
  height: 60px;
  margin-bottom: 10px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #D5B69D;
}

.input-focus {
  border-color: #a0522d;
  box-shadow: 0 0 5px rgba(160, 82, 45, 0.8);
  outline: none;
}

.btn-danger {
  background-color: #a6433f;
  color: #ffffff;
  border: none;
}
</style>
