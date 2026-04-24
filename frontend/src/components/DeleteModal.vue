<template>
  <div v-if="open" class="overlay">

    <div class="modal">

      <h3>Удалить деталь?</h3>
      <p>{{ part?.name }}</p>

      <div class="actions">
        <button @click="confirmDelete" class="btn-delete">
          Удалить
        </button>

        <button @click="$emit('close')" class="btn-cancel">
          Отмена
        </button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { usePartsStore } from "../store/parts";

const props = defineProps({
  open: Boolean,
  part: Object
});

const emit = defineEmits(["close"]);

const store = usePartsStore();

const confirmDelete = async () => {
  await store.deletePart(props.part.id);
  emit("close");
};
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 300px;
}

.actions {
  display: flex;
  justify-content: space-between;
}

.btn-delete {
  background: #ef4444;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
}
</style>