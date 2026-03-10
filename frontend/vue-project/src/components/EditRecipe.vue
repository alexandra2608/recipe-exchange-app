<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}

const route = useRoute();
const router = useRouter();
const recipe = ref({
  title: '',
  description: '',
  instructions: '',
  complexity: '',
  image: null,
  video: null,
  tags: [],
});
const tags = ref([]);

const loadRecipe = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/recipes/${route.params.id}/`);
    const data = response.data;
    recipe.value = {
      title: data.title,
      description: data.description,
      instructions: data.instructions,
      complexity: data.complexity,
      image: data.image,
      video: data.video,
      tags: data.tags,
    };
  } catch (error) {
    console.error('Ошибка загрузки рецепта:', error);
  }
};

const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tags/');
    tags.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error);
  }
};

const handleFileUpload = (e, field) => {
  recipe.value[field] = e.target.files[0];
};

const updateRecipe = async () => {
  const formData = new FormData();

  for (const key in recipe.value) {
    if (key === 'tags') {
      recipe.value[key].forEach(tagId => formData.append('tags', tagId));
    } else if (recipe.value[key] !== null) {
      formData.append(key, recipe.value[key]);
    }
  }

  try {
    await axios.put(`http://localhost:8000/recipes/${route.params.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    });

    router.push(`/profile`);
  } catch (error) {
    console.error('Ошибка обновления рецепта:', error.response?.data || error);
  }
};

const cancel = () => {
  router.push('/profile');
};

onMounted(() => {
  loadRecipe();
  loadTags();
});
</script>

<template>
  <header class="header">
    <div class="brand d-flex align-items-center">
      <a href="/" class="d-flex align-items-center logo-link">
        <img src="../assets/icons/recipe-book.png" alt="Logo" class="logo me-2" />
        <span>Culinarity</span>
      </a>
    </div>
    <div class="theme-switcher">
        <label for="themeToggle" class="form-check-label">Тема</label>
        <input
          type="checkbox"
          id="themeToggle"
          class="form-check-input"
          @change="toggleTheme"
          aria-label="Переключатель темы"
        />
      </div>
    <nav class="icons">
      <a href="/profile" aria-label="Профиль пользователя">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#person-circle"></use>
        </svg>
      </a>
      <a href="/add/recipe" aria-label="Добавить рецепт">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#plus-circle-fill"></use>
        </svg>
      </a>
    </nav>
  </header>
  <div class="container">
    <div class="registration-container">
      <h1 class="text-center">Редактировать рецепт</h1>
      <form @submit.prevent="updateRecipe">
        <div class="form-group">
          <label for="title" class="form-label"><strong>Название</strong></label>
          <input type="text" id="title" v-model="recipe.title" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="description" class="form-label"><strong>Ингредиенты</strong></label>
          <textarea id="description" v-model="recipe.description" class="form-control" rows="3" required></textarea>
        </div>

        <div class="form-group">
          <label for="instructions" class="form-label"><strong>Инструкции</strong></label>
          <textarea id="instructions" v-model="recipe.instructions" class="form-control" rows="5" required></textarea>
        </div>

        <div class="form-group">
          <label for="complexity" class="form-label"><strong>Сложность</strong></label>
          <select id="complexity" v-model="recipe.complexity" class="form-control" required>
            <option value="easy">Легко</option>
            <option value="medium">Средне</option>
            <option value="hard">Трудно</option>
          </select>
        </div>

        <div class="form-group">
          <label for="tags" class="form-label"><strong>Теги</strong></label>
          <select id="tags" v-model="recipe.tags" class="form-control" multiple>
            <option v-if="tags.length === 0" disabled>Нет доступных тегов</option>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="image" class="form-label"><strong>Изображение</strong></label>
          <input
            type="file"
            id="image"
            @change="(e) => handleFileUpload(e, 'image')"
            class="form-control-file"
          />
        </div>

        <div class="form-group">
          <label for="video" class="form-label"><strong>Видео</strong></label>
          <input
            type="file"
            id="video"
            @change="(e) => handleFileUpload(e, 'video')"
            class="form-control-file"
          />
        </div>

        <button type="submit" class="btn register-btn">Обновить рецепт</button>
        <button @click="cancel" class="btn btn-secondary mt-2">Отменить</button>
      </form>
    </div>
  </div>
</template>

<style scoped>

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: var(--header-bg-color) ;
    color: var(--header-text-color);
    flex-wrap: wrap;
}


header .brand {
    font-family: Quicksand, sans-serif;
    font-size: 24px;
    font-weight: bold;
    color: var(--header-text-color);
}

.icons svg {
    width: 30px;
    height: 30px;
    fill: currentColor;
    cursor: pointer;
    transition: transform 0.2s ease;
    margin-right: 20px;
}


.icons a {
    color: var(--header-text-color);
}

.icons svg:hover {
  transform: scale(1.1);
}

.icons button {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
}

.logo {
    width: 40px;
    height: auto;
}

.logo-link {
    text-decoration: none;
    color: inherit;
}

.logo-link:hover {
    text-decoration: none;
    color: inherit;
}

body {
  font-family: Quicksand, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.registration-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background-color: var(--form-bg-color);
  border-radius: 15px;
  box-shadow: 0 0 10px var(--form-border-color);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--text-center-color);
}

.form-group {
  margin-bottom: 15px;
}

textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  resize: vertical;
}

button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.register-btn {
  background-color: var(--btn-bg-color);
  color: #fff;
}

.register-btn:hover {
  background-color: var(--btn-hover-color);
}

.register-btn:focus {
  background-color: var(--btn-hover-color);
}

.btn-secondary {
  background-color: #f0ad4e;
}

.btn-secondary:hover {
  background-color: #ec971f;
}

</style>
