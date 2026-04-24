<template>
  <div v-if="open" class="overlay">

    <div class="modal">

      <h3>{{ isEdit ? "Редактировать" : "Добавить" }} деталь</h3>

      <input v-model="name" placeholder="Название" class="input" />
      <input v-model.number="price" placeholder="Цена" class="input" />
      <input v-model.number="quantity" placeholder="Количество" class="input" />

      <div class="actions">
        <button @click="submit" class="btn-primary">
          {{ isEdit ? "Сохранить" : "Добавить" }}
        </button>

        <button @click="$emit('close')" class="btn-cancel">
          Отмена
        </button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { usePartsStore } from "../store/parts";

const props = defineProps({
  open: Boolean,
  part: Object,
  parentId: Number
});

const emit = defineEmits(["close"]);

const store = usePartsStore();

const name = ref("");
const price = ref(0);
const quantity = ref(1);

const isEdit = ref(false);

watch(() => props.open, () => {
  if (props.part) {
    // EDIT
    isEdit.value = true;
    name.value = props.part.name;
    price.value = props.part.price || 0;
    quantity.value = props.part.quantity || 1;
  } else {
    // ADD
    isEdit.value = false;
    name.value = "";
    price.value = 0;
    quantity.value = 1;
  }
});

const submit = async () => {
  if (!name.value) return;

  if (isEdit.value) {
    await store.updatePart(props.part.id, {
      name: name.value,
      price: price.value,
      quantity: quantity.value
    });
  } else {
    await store.createPart({
      name: name.value,
      price: price.value,
      quantity: quantity.value,
      parent_id: props.parentId
    });
  }

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
  width: 320px;
}

.input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.actions {
  display: flex;
  justify-content: space-between;
}
</style>