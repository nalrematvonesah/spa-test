<template>
  <div>
    <div style="margin-bottom: 10px">
      <button @click="downloadExcel" class="btn">Excel</button>
      <button @click="downloadPDF" class="btn">PDF</button>
    </div>
    <h2>Детали автомобиля</h2>

    <PartForm />

    <div class="table-header">
      <div>Деталь</div>
      <div>Цена</div>
      <div>Кол-во</div>
      <div>Стоимость</div>
      <div>Действия</div>
    </div>

    <PartRow
      v-for="(node, i) in store.tree"
      :key="node.id"
      :node="node"
      :level="0"
      :index="(i+1).toString()"
    />

  </div>
</template>

<script setup>

import { onMounted } from "vue";
import { usePartsStore } from "../store/parts";
import PartRow from "../components/PartRow.vue";
import PartForm from "../components/PartForm.vue";

const store = usePartsStore();

const downloadFile = async (url, filename) => {
  try {
    const res = await fetch(url);

    if (!res.ok) {
      throw new Error("Download failed");
    }

    const blob = await res.blob();

    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();

    window.URL.revokeObjectURL(link.href);
  } catch (e) {
    console.error(e);
    alert("Ошибка скачивания");
  }
};

const downloadExcel = () => {
  window.open("/api/export/excel");
};

const downloadPDF = () => {
  window.open("/api/export/pdf");
};
onMounted(() => {
  store.fetchTree();
});
</script>