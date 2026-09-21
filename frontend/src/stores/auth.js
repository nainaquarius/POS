import { defineStore } from "pinia";
import api from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post("/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      this.token = response.data.access_token;

      // Get the logged-in user's profile
      const profileResponse = await api.get("/auth/profile", {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      });

      this.user = profileResponse.data;

      // Save token and user
      localStorage.setItem("token", this.token);
      localStorage.setItem("user", JSON.stringify(this.user));
    },

    logout() {
      this.token = null;
      this.user = null;

      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    loadUser() {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");

      if (token) {
        this.token = token;
      }

      if (user) {
        this.user = JSON.parse(user);
      }
    },
  },
});