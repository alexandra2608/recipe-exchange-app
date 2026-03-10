<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import cookingImage from '@/assets/images/cooking.png';
import { useRecipeUtils } from '@/composables/useRecipeUtils';
import router from "@/router/index.js";
import Modal from "@/components/Modal.vue";

const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const { getCurrentUserId } = useRecipeUtils();
const recipes = ref([]);

const fetchRecipes = async () => {
  try {
    const userId = await getCurrentUserId();
    const response = await axios.get(`http://127.0.0.1:8000/users/${userId}/recipes/`);
    recipes.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке рецептов:", error);
  }
};

const editRecipe = (recipeId) => {
  router.push(`/edit/recipe/${recipeId}`);
};


const deleteRecipe = async (recipeId) => {
  if (!window.confirm("Вы уверены, что хотите удалить этот рецепт?")) {
    return;
  }

  try {
    await axios.delete(`http://127.0.0.1:8000/recipes/${recipeId}/`);
    recipes.value = recipes.value.filter(recipe => recipe.id !== recipeId);
    showSuccessModal("Рецепт успешно удалён!");
  } catch (error) {
    console.error("Ошибка при удалении рецепта:", error);
    showSuccessModal("Не удалось удалить рецепт. Пожалуйста, попробуйте снова.");
  }
};

onMounted(() => {
  fetchRecipes();
});
</script>

<template>
  <section>
    <h3>Мои рецепты</h3>
    <div class="row">
      <div v-for="recipe in recipes" :key="recipe.id" class="col-md-4">
        <div class="recipe-card">
          <a :href="'/recipes/' + recipe.id">
          <img
            :src="recipe.image ? recipe.image : cookingImage"
            :alt="recipe.title"
            class="recipe-image img-fluid"
          />
          </a>
          <h5 class="recipe-title">{{ recipe.title }}</h5>
          <ul class="ingredient-list">
            <li v-for="ingredient in recipe.description.split('\r\n')" :key="ingredient">{{ ingredient }}</li>
          </ul>
          <button @click="editRecipe(recipe.id)" class="btn btn-warning">Редактировать</button><button @click="deleteRecipe(recipe.id)" class="btn btn-danger">Удалить</button>
        </div>
      </div>
    </div>
    <Modal
      :isVisible="showModal"
      :message="modalMessage"
      @close="showModal = false"
    />
  </section>
</template>

<style scoped>
.btn-warning {
  background-color: #e8d2ae;
  color: #5B4D42;
  font-weight: bold;
  border: none;
  margin-right: 10px;
}

.btn-danger {
  background-color: #a6433f;
  color: #ffffff;
  border: none;
}
</style>
