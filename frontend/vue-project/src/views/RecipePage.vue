<script setup>
import Header from "@/components/Header.vue";
import RecipeInfo from "@/components/RecipePage/RecipeInfo.vue";
import SaveRateRecipe from "@/components/RecipePage/SaveRecipe.vue";
import RateRecipe from "@/components/RecipePage/RateRecipe.vue";
import CommentRecipe from "@/components/RecipePage/CommentRecipe.vue";
</script>

<template>
  <Header />
  <div class="recipe-container">
    <main>
      <RecipeInfo />
      <SaveRateRecipe />
      <RateRecipe />
      <CommentRecipe />
    </main>
  </div>
</template>

<style>
.recipe-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: var(--recipe-bg-color);
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.save-button {
  display: inline-block;
  background-color: var(--divider-color);
  color: var(--bg-color);
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
}
.save-button:hover {
  background-color: var(--btn-hover-color);
}
</style>
