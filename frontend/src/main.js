import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import axios from 'axios'

// 默认后端地址：优先使用环境变量 `VITE_API_BASE`，否则使用相对路径（方便其他机器访问托管前端时请求同一主机）
axios.defaults.baseURL = import.meta.env.VITE_API_BASE || ''

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
import TaskList from './pages/TaskList.vue'
import Publish from './pages/Publish.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import TaskDetail from './pages/TaskDetail.vue'
import Profile from './pages/Profile.vue'
import './styles.css'

const routes = [
  { path: '/', component: TaskList },
  { path: '/publish', component: Publish },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/task/:id', component: TaskDetail },
  { path: '/profile', component: Profile },
]

const router = createRouter({ history: createWebHistory(), routes })

// 全局路由守卫：默认入口为登录页，若本地存在 token 则允许访问其他页面
router.beforeEach((to, from, next) => {
  const publicPaths = ['/login','/register']
  const token = localStorage.getItem('access')
  if (!token && !publicPaths.includes(to.path)) {
    return next('/login')
  }
  if (token && to.path === '/login') {
    return next('/')
  }
  next()
})

createApp(App).use(createPinia()).use(router).mount('#app')
