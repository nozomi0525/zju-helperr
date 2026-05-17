<template>
  <div>
    <div class="card">
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
    <div class="card" v-for="t in tasks" :key="t.id">
      <div class="task-item">
        <div>
          <div style="font-weight:600">{{t.title}}</div>
          <div style="color:#64748b">{{t.category}} · {{t.location}} · {{t.status}}</div>
        </div>
        <div>
          <router-link :to="`/task/${t.id}`" class="btn btn-link">查看</router-link>
          <button class="btn" @click="accept(t)" v-if="logged">接单</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {tasks:[],category:'',logged:false}}
  ,methods:{
    async load(){
      let url='/api/tasks/'
      if(this.category) url+='?category='+encodeURIComponent(this.category)
      const r=await axios.get(url)
      this.tasks=r.data
    },
    async accept(t){
      try{
        const token=localStorage.getItem('access')
        if(!token){alert('请先登录');return}
        await axios.post('/api/orders/',{task:t.id},{headers:{Authorization:'Bearer '+token}})
        alert('接单成功')
      }catch(e){alert('接单失败')}
    }
  },
  mounted(){this.load();this.logged=!!localStorage.getItem('access')}
}
</script>
