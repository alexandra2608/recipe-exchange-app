<script setup>
import {useRouter} from "vue-router";
import {ref} from "vue";
import Modal from "@/components/Modal.vue";

const router = useRouter();
const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const logout = () => {
  localStorage.removeItem("auth_token");
  showSuccessModal("Вы успешно вышли из профиля.");
  setTimeout(() => {
    router.push("/");
  }, 1000);
};
function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}
const SearchFilters = () => {
  router.push("/search");
};

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
      <button id="logout-btn" type="button" class="icons" aria-label="Выйти" @click="logout">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#box-arrow-in-right"></use>
        </svg>
      </button>
    </nav>
    <Modal
      :isVisible="showModal"
      :message="modalMessage"
      @close="showModal = false"
    />
  </header>
</template>

<style>

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

.search-bar {
  flex: 1 1 33%;
  max-width: 500px;
  min-width: 150px;
  margin: 10px;
}
</style>
