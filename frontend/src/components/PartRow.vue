<template>
  <div>

    <div class="row">

      <div :style="{ paddingLeft: level * 20 + 'px' }">
        {{ index }} {{ node.name }}
      </div>

      <div>{{ displayPrice }}</div>
      <div>{{ node.quantity || 1 }}</div>
      <div>{{ node.total_price }}</div>

      <div class="actions">

        <button @click="openAdd" class="btn-add">+</button>
        <button @click="openEdit" class="btn-edit">✏️</button>
        <button @click="openDelete" class="btn-delete">🗑</button>

      </div>

    </div>

    <PartRow
      v-for="(child, i) in node.children"
      :key="child.id"
      :node="child"
      :level="level + 1"
      :index="index + '.' + (i+1)"
    />

    <!-- МОДАЛКИ -->
    <PartModal
      :open="showModal"
      :parentId="node.id"
      :part="editPart"
      @close="closeModal"
    />

    <DeleteModal
      :open="showDelete"
      :part="node"
      @close="showDelete = false"
    />

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { usePartsStore } from "../store/parts";
import PartModal from "./PartModal.vue";
import DeleteModal from "./DeleteModal.vue";

const props = defineProps({
  node: Object,
  level: Number,
  index: String
});

const store = usePartsStore();

const showModal = ref(false);
const showDelete = ref(false);
const editPart = ref(null);

const displayPrice = computed(() => {
  return props.node.children?.length
    ? props.node.total_price
    : props.node.price || 0;
});

/* actions */
const openAdd = () => {
  editPart.value = null;
  showModal.value = true;
};

const openEdit = () => {
  editPart.value = props.node;
  showModal.value = true;
};

const openDelete = () => {
  showDelete.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editPart.value = null;
};
</script>