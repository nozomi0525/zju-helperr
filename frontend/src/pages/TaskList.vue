<template>
  <div>
    <div class="card">
      <div class="card-header">
        <h3>任务列表</h3>
        <div class="subtitle">筛选你感兴趣的任务，并快速刷新最新任务</div>
      </div>
      <div class="form-row">
        <select v-model="category">
          <option value="">全部</option>
          <option value="carpool">拼车</option>
          <option value="errand">跑腿</option>
          <option value="agency">代办</option>
          <option value="emergency">特需</option>
        </select>
        <button class="btn" @click="load">刷新</button>
      </div>
    </div>

    <div class="card empty-state" v-if="tasks.length === 0">暂无任务，稍后再试或点击刷新</div>

    <div class="card task-card" v-for="t in tasks" :key="t.id">
      <div class="task-item">
        <div class="task-meta">
          <div class="task-title">{{ t.title }}</div>
          <div class="task-info">{{ t.category }} · {{ t.location }} · <span class="status">{{ t.status }}</span></div>
        </div>
        <div class="task-actions">
          <router-link :to="`/task/${t.id}`" class="btn ghost">查看</router-link>
          <button class="btn" @click="accept(t)" v-if="logged">接单</button>
        </div>
      </div>
      <div class="task-footer">
        <span class="pill">类别：{{ t.category }}</span>
        <span class="tag">状态：{{ t.status }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      tasks: [],
      category: '',
      logged: false
    }
  },
  methods: {
    async load() {
      let url = '/api/tasks/'
      if (this.category) url += '?category=' + encodeURIComponent(this.category)
      const r = await axios.get(url)
      this.tasks = r.data
    },
    async accept(t) {
      try {
        const token = localStorage.getItem('access')
        if (!token) {
          alert('请先登录')
          return
        }
        await axios.post('/api/orders/', { task: t.id }, { headers: { Authorization: 'Bearer ' + token } })
        alert('接单成功')
      } catch (e) {
        alert('接单失败')
      }
    }
  },
  mounted() {
    this.load()
    this.logged = !!localStorage.getItem('access')
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}
.card-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 1.15rem;
}
.subtitle {
  margin: 0;
  color: #64748b;
  font-size: 0.95rem;
}
.task-card {
  padding: 0;
  overflow: hidden;
}
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
}
.task-meta {
  min-width: 0;
}
.task-title {
  font-weight: 700;
  color: #1e293b;
  font-size: 1rem;
}
.task-info {
  margin-top: 6px;
  color: #64748b;
  font-size: 0.95rem;
}
.status {
  font-weight: 600;
  color: #4338ca;
}
.task-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.task-actions .btn {
  min-width: 72px;
}
.task-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  padding: 12px 20px 18px;
  background: #f8fafc;
}
.pill,
.tag {
  display: inline-flex;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
}
.pill {
  background: #eef2ff;
  color: #3730a3;
}
.tag {
  background: #f1f5f9;
  color: #475569;
}
.empty-state {
  text-align: center;
  color: #475569;
}
@media (max-width: 680px) {
  .task-item {
    flex-direction: column;
    align-items: stretch;
  }
  .task-actions {
    justify-content: flex-end;
    width: 100%;
  }
}
</style>
