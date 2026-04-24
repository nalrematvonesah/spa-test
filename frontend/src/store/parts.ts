import { defineStore } from "pinia";

const API = "/api";

export const usePartsStore = defineStore("parts", {
  state: () => ({
    tree: [] as any[]
  }),

  actions: {
    async fetchTree() {
      const res = await fetch(`${API}/parts`);
      this.tree = await res.json();
    },

    async createPart(data: any) {
      await fetch(`${API}/parts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      await this.fetchTree();
    },

    async deletePart(id: number) {
      await fetch(`${API}/parts/${id}`, {
        method: "DELETE"
      });
      await this.fetchTree();
    },

    async updatePart(id: number, data: any) {
      await fetch(`${API}/parts/${id}`, {
        method: "PATCH", 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      await this.fetchTree();
    }
  }
});