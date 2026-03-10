<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useRecipeUtils } from '@/composables/useRecipeUtils';
import Modal from "@/components/Modal.vue";

const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const { getCurrentUserId, fetchRecipeById } = useRecipeUtils();

const route = useRoute();
const recipe = ref(null);
const savedRecipes = ref([]);
const isSaved = ref(false);

const fetchRecipe = async (id) => {
  try {
    recipe.value = await fetchRecipeById(id);
    await fetchSavedRecipes();
  } catch (error) {
    console.error("Ошибка при загрузке рецепта:", error);
  }
};

const fetchSavedRecipes = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    const response = await axios.get('http://localhost:8000/save-recipe/', {
      headers: { Authorization: `Bearer ${token}` },
    });

    savedRecipes.value = response.data;
    checkIfRecipeSaved();
  } catch (error) {
    console.error("Ошибка при получении сохранённых рецептов:", error);
  }
};


const checkIfRecipeSaved = () => {
  const savedRecipe = savedRecipes.value.find(
    (saved) => saved.recipe === recipe.value.id
  );
  isSaved.value = !!savedRecipe;
};

const toggleSaveRecipe = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      showSuccessModal("Вы не авторизованы! Пожалуйста, войдите в систему.");
      return;
    }

    const userId = await getCurrentUserId();
    if (!userId || !recipe.value?.id) {
      showSuccessModal("Невозможно выполнить действие.");
      return;
    }

    if (recipe.value.author?.id === userId) {
      showSuccessModal("Вы не можете сохранить свой собственный рецепт.");
      return;
    }

    if (isSaved.value) {
      const savedRecipe = savedRecipes.value.find(
        (saved) => saved.recipe === recipe.value.id && saved.user === userId
      );

      if (savedRecipe) {
        await axios.delete(`http://localhost:8000/save-recipe/${savedRecipe.id}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        showSuccessModal("Рецепт удалён из сохранённых.");
      }
    } else {
      await axios.post(
        'http://localhost:8000/save-recipe/',
        { user: userId, recipe: recipe.value.id },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      showSuccessModal("Рецепт сохранён в профиль.");
    }

    await fetchSavedRecipes();
  } catch (error) {
    console.error("Ошибка при изменении сохранения рецепта:", error);
  }
};

onMounted(() => {
  const recipeId = route.params.id;
  fetchRecipe(recipeId);
});
</script>

<template>
  <div v-if="recipe">
    <button @click="toggleSaveRecipe" class="save-button">
      {{ isSaved ? "Уже в профиле" : "Сохранить рецепт" }}
    </button>
  </div>
  <div v-else>
    <p>Загрузка...</p>
  </div>
  <Modal
      :isVisible="showModal"
      :message="modalMessage"
      @close="showModal = false"
    />
</template>

<style scoped>

</style>
