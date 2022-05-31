export default {
  clear() {
    window.localStorage.setItem("token", "");
  },
  saveToken(token) {
    window.localStorage.setItem("token", token);
  },
  getToken() {
    return window.localStorage.getItem("token");
  },
};
