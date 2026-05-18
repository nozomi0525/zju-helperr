<template>
  <div id="app-root">
    <header class="header">
      <div class="brand">浙大校园互助</div>
      <nav>
        <router-link to="/">帖子</router-link>
        <router-link to="/publish">发布</router-link>
        <router-link to="/profile">我的</router-link>
      </nav>
      <div class="user-area">
        <template v-if="isLoggedIn">
          <button class="btn btn-logout" @click="logout">退出登录</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn-ghost">登录</router-link>
          <router-link to="/register" class="btn btn-ghost">注册</router-link>
        </template>
      </div>
    </header>
    <main class="container">
      <router-view />
    </main>
    <footer class="footer">© 浙大校园互助</footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(!!localStorage.getItem('access'))

function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  isLoggedIn.value = false
  router.push('/login')
}

onMounted(()=>{
  router.afterEach(()=>{
    isLoggedIn.value = !!localStorage.getItem('access')
  })
})
</script>
