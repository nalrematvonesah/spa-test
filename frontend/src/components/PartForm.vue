<template>
  <div style="margin-bottom:10px">

    <input v-model="name" placeholder="Название" class="input" />
    <input v-model.number="price" placeholder="Цена" class="input" />
    <input v-model.number="quantity" placeholder="Кол-во" class="input" />

    <button @click="submit" class="btn btn-primary">
      Добавить
    </button>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { usePartsStore } from "../store/parts";

const store = usePartsStore();

const name = ref("");
const price = ref(0);
const quantity = ref(1);

const submit = async () => {
  if (!name.value) return;

  await store.createPart({
    name: name.value,
    price: price.value,
    quantity: quantity.value
  });

  name.value = "";
};
</script>