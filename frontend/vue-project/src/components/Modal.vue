<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  isVisible: Boolean,
  message: String,
});

const emits = defineEmits(["close"]);

const closeModal = () => {
  emits("close");
};
</script>

<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h3 class="modal-title">Уведомление</h3>
      <div class="modal-body">
        {{ message }}
      </div>
      <button class="btn register-btn" @click="closeModal">Закрыть</button>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: #FFFAF3;
  border-radius: 10px;
  border: 1px solid #946A49;
  padding: 20px;
  width: 300px;
  text-align: center;
}

.modal-title {
  font-family: Quicksand, sans-serif;
  font-size: 20px;
  font-weight: bold;
  color: #946A49;
}

.modal-body {
  font-family: Quicksand, sans-serif;
  color: #9C7F68;
  padding: 20px;
}

.register-btn {
  background-color: var(--btn-bg-color);
  color: #fff;
  border: none;
  border-radius: 10px;
  width: 100%;
  padding: 10px;
  font-weight: bold;
  font-size: 18px;
  transition: background-color 0.3s;
}

.register-btn:hover {
  background-color: var(--btn-hover-color);
  color: #fff;
}
</style>
