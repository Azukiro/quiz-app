<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>

    <div class="wrapper">
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">

        <RouterLink class="navbar-brand" to="/">
          <img src="/src/components/icons/icon.png" height="75" alt="Icon">
        </RouterLink>
        <ul class="navbar-nav">
          <li class="nav-item active">
            <RouterLink class="nav-link" to="/">Home</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style>
html,
body {
  font-family: 'Fira Mono', sans-serif;
  background-color: rgb(24, 24, 31);
  color: rgb(226, 226, 226);
}

.my-custom-scrollbar {
  position: relative;
  height: 400px;
  overflow: auto;
}

.table-wrapper-scroll-y {
  display: block;
}
</style>
