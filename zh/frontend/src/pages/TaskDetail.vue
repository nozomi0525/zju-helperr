<template>
  <div class="card">
    <h3>{{task.title}}</h3>
    <div>分类：{{task.category}}</div>
    <div>位置：{{task.location}}</div>
    <div>备注：{{task.remark}}</div>
    <div style="margin-top:12px">
      <button class="btn" @click="accept" v-if="logged">接单</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {task:{},logged:false}},
  async mounted(){
    const id=this.$route.params.id
    const r=await axios.get('/api/tasks/'+id+'/')
    this.task=r.data
    this.logged=!!localStorage.getItem('access')
  },
  methods:{
    async accept(){
      try{
        const token=localStorage.getItem('access')
        await axios.post('/api/orders/',{task:this.task.id},{headers:{Authorization:'Bearer '+token}})
        alert('接单成功')
        this.$router.push('/')
      }catch(e){alert('失败')}
    }
  }
}
</script>
