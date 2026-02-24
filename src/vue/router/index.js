import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import LoginView from '../views/auth/LoginView.vue'
import CommitmentView from '../views/about/CommitmentView.vue'

const routes = [
    { path: '/', name: 'home', component: IndexView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/commitment', name: 'commitment', component: CommitmentView }
]

export default createRouter({
    history: createWebHistory(),
    routes
})
