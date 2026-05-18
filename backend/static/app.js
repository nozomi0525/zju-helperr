const { createApp, ref } = Vue;

createApp({
  data(){
    return {
      showTab: 'list',
      tasks: [],
      filter: {category: ''},
      form: {category:'carpool', title:'', location:'', remark:''},
      user: null,
      showLogin:false, showRegister:false,
      auth: {username:'', password:''},
      reg: {username:'', password:''},
    }
  },
  methods: {
    authHeader(){
      const token = localStorage.getItem('access');
      return token ? {'Authorization': 'Bearer ' + token} : {};
    },
    async load(){
      let url = '/api/tasks/';
      if(this.filter.category) url += '?category=' + encodeURIComponent(this.filter.category);
      const res = await fetch(url);
      this.tasks = await res.json();
    },
    async publish(){
      if(!this.user){alert('请先登录'); return}
      const payload = {category:this.form.category,title:this.form.title,template_data:{},location:this.form.location,remark:this.form.remark};
      const res = await fetch('/api/tasks/',{method:'POST',headers:{'Content-Type':'application/json',...this.authHeader()},body:JSON.stringify(payload)});
      if(res.ok){this.form.title='';this.form.location='';this.form.remark='';this.showTab='list';this.load();}
      else {alert('发布失败')}
    },
    async login(){
      const res = await fetch('/api/token/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:this.auth.username,password:this.auth.password})});
      if(res.ok){const data=await res.json();localStorage.setItem('access',data.access);localStorage.setItem('refresh',data.refresh);this.showLogin=false;await this.fetchMe();this.load();}
      else {alert('登录失败')}
    },
    async register(){
      try{
        console.log('Attempting register', this.reg)
        const res = await fetch('/api/users/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:this.reg.username,password:this.reg.password})});
        const text = await res.text()
        console.log('Register response', res.status, text)
        if(res.ok){alert('注册成功，请登录');this.showRegister=false;} else {alert('注册失败: '+text)}
      }catch(e){
        console.error('Register error', e)
        alert('注册异常: '+e.message)
      }
    },
    async fetchMe(){
      const res = await fetch('/api/users/me/');
      if(res.ok){this.user = await res.json();} else {this.user = null}
    },
    logout(){localStorage.removeItem('access');localStorage.removeItem('refresh');this.user=null},
    async accept(task){
      if(!this.user){alert('请登录');return}
      const res = await fetch('/api/orders/',{method:'POST',headers:{'Content-Type':'application/json',...this.authHeader()},body:JSON.stringify({task:task.id})});
      if(res.ok){alert('已接单');this.load()} else {const t=await res.text();alert('接单失败: '+t)}
    },
    openTask(t){alert(JSON.stringify(t,null,2))}
  },
  async mounted(){
    await this.load();
    const token = localStorage.getItem('access');
    if(token) await this.fetchMe();
  }
}).mount('#app');
