<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import Modal from "@/components/Modal.vue";

const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const route = useRoute();
const recipe = ref(null);
const userRating = ref(null);
const averageRating = ref(null);
const selectedRating = ref(null);
const isAuthor = ref(false);
import { useRecipeUtils } from '@/composables/useRecipeUtils';

const { getCurrentUserId } = useRecipeUtils();

const fetchRecipeMetrics = async (recipeId) => {
  try {
    const response = await axios.get('http://localhost:8000/recipes/metrics/');
    const metrics = response.data.find((item) => item.id === recipeId);

    if (metrics) {
      averageRating.value = metrics.average_rating ?? 'Нет оценок';
    } else {
      averageRating.value = 'Нет оценок';
    }
  } catch (error) {
    console.error('Ошибка получения метрик рецепта:', error);
    averageRating.value = 'Ошибка загрузки';
  }
};

const fetchRecipe = async (recipeId) => {
  try {
    const response = await axios.get(`http://localhost:8000/recipes/${recipeId}/`);
    recipe.value = response.data;

    const userId = await getCurrentUserId();
    isAuthor.value = recipe.value.author?.id === userId;

    fetchRecipeMetrics(recipeId);
    fetchUserRating(recipeId);
  } catch (error) {
    console.error('Ошибка при загрузке рецепта:', error);
  }
};

const fetchUserRating = async (recipeId) => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    const userId = await getCurrentUserId();
    const response = await axios.get('http://localhost:8000/ratings/', {
      headers: { Authorization: `Bearer ${token}` },
    });

    const userRatingData = response.data.find(
      (rating) => rating.recipe === recipeId && rating.user === userId
    );

    if (userRatingData) {
      userRating.value = userRatingData;
      selectedRating.value = userRatingData.rating_value;
    } else {
      userRating.value = null;
      selectedRating.value = null;
    }
  } catch (error) {
    console.error('Ошибка получения оценки пользователя:', error);
  }
};

const submitRating = async () => {
  try {
    if (isAuthor.value) {
      showSuccessModal('Вы не можете оценивать свой собственный рецепт.');
      return;
    }

    const token = localStorage.getItem('auth_token');
    if (!token) {
      showSuccessModal('Вы не авторизованы! Пожалуйста, войдите в систему.');
      return;
    }

    const userId = await getCurrentUserId();
    if (!userId || !recipe.value?.id) {
      showSuccessModal('Невозможно выполнить действие.');
      return;
    }

    if (!selectedRating.value) {
      showSuccessModal('Пожалуйста, выберите оценку.');
      return;
    }

    if (userRating.value) {
      await axios.put(
        `http://localhost:8000/ratings/${userRating.value.id}/`,
        { rating_value: selectedRating.value, recipe: recipe.value.id, user: userId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showSuccessModal('Ваша оценка обновлена.');
    } else {
      await axios.post(
        'http://localhost:8000/ratings/',
        { user: userId, recipe: recipe.value.id, rating_value: selectedRating.value },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      showSuccessModal('Ваша оценка добавлена.');
    }

    fetchRecipeMetrics(recipe.value.id);
    fetchUserRating(recipe.value.id);
  } catch (error) {
    console.error('Ошибка при добавлении или изменении оценки:', error);
  }
};

onMounted(() => {
  const recipeId = parseInt(route.params.id, 10);
  if (!isNaN(recipeId)) {
    fetchRecipe(recipeId);
  } else {
    console.error('Некорректный ID рецепта.');
  }
});
</script>

<template>
  <div>
    <p><strong>Средняя оценка: {{ averageRating }}</strong></p>

    <div v-if="isAuthor">
      <p>Вы не можете оценить свой рецепт!</p>
    </div>

    <div v-else>
      <label for="rating-select">Ваша оценка:</label>
      <select id="rating-select" v-model="selectedRating">
        <option disabled value="">Выберите оценку</option>
        <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
      </select>
      <button @click="submitRating" class="btn-warning">Оценить</button>
    </div>

    <p v-if="userRating">Ваша текущая оценка: {{ userRating.rating_value }}</p>
  </div>
  <Modal
      :isVisible="showModal"
      :message="modalMessage"
      @close="showModal = false"
    />
</template>

<style scoped>
.btn-warning {
  background-color: #e8d2ae;
  color: #5B4D42;
  font-weight: bold;
  border: none;
  margin-right: 10px;
  margin-left: 5px;
  border-radius: 5px;
}

p {
  margin-top: 10px;
}

label {
  margin-right: 5px;
}
</style>
