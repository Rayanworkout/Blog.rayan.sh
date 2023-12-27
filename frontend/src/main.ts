import { createApp } from 'vue'

// Import the router to create multiple pages 
import { Router, createRouter, createWebHistory } from 'vue-router';

// Import the pages
import Home from './pages/Home.page.vue'
import About from './pages/About.page.vue'
import Article from './pages/Article.page.vue'



import './style.css'
// Bootstrap css and bootstrap icons
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css'
import App from './App.vue'



// Create a custom type for the $router property
// So it can be used in any component without errors
declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        $router: Router;
    }
}

// I create a router to manage my pages
const router = createRouter({
    history: createWebHistory(),
    routes: [
        // On sections within the same page, I use smooth scrollBehavior
        { path: '/', component: Home, name: 'Home' },
        { path: '/about', component: About, name: 'About' },
        { path: '/article/:id', component: Article, name: 'Article' },
    ],

    scrollBehavior(to, _, savedPosition) {
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth'
            };
        } else if (savedPosition) {
            return savedPosition;
        } else {
            return { left: 0, top: 0 };
        }
    }
});

createApp(App).use(router).mount('#app')
