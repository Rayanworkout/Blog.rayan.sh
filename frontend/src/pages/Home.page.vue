<script setup lang="ts">
// Components
import MyHeader from './components/Header.component.vue'
import ArticlesGrid from './components/ArticlesGrid.component.vue'
import SearchInput from './components/SearchInput.component.vue'
import CategoriesFilter from './components/CategoriesFilter.component.vue'

// Services
import { fetchArticles, fetchCategoryList } from '../services/api.service.ts'
import { handleCategoryClicked } from '../services/filtering.service.ts'

// Built-in Vue functions
import { onMounted, reactive, ref } from 'vue'

// Types
import { ArticleInGridType } from '../types/article.type.ts'


// Initialize reactive variables
const articles = ref<ArticleInGridType[]>([])
const filteredArticles = ref<ArticleInGridType[]>([])

const allCategories = ref<string[]>([]);
const filteredCategories = ref<string[]>([]);

const state = reactive({
  loading: true,
  error: false
})

fetchArticles(state, articles);

onMounted(async () => {

  allCategories.value = await fetchCategoryList();
  // Add "ALL" category to the beginning of the list
  allCategories.value.unshift("ALL");

  // I use setTimeout to wait for the articles to be fetched
  setTimeout(() => {
    // Initialize filtered articles with all articles
    filteredArticles.value = articles.value;
  }, 200);

});


// Apply filtering with the imported function
const applyFiltering = (category: string) => {
  handleCategoryClicked(category, filteredCategories, articles, filteredArticles);
}

const handleInput = (input: string) => {
  // Allowing the user to search for articles by title
  if (input.length < 2) {
    filteredArticles.value = articles.value;
    return;
  }
  filteredArticles.value = articles.value.filter(article => {
    // filter either by title or by description content
    const searchTerm = input.toLowerCase();
    const inTitle = article.title.toLowerCase().includes(searchTerm);
    const inContent = article.description.toLowerCase().includes(searchTerm);
    
    return inTitle || inContent;
});
}

</script>

<template>
  <MyHeader />
  <SearchInput @inputUpdate="handleInput" />
  <CategoriesFilter @categoryClicked="applyFiltering" :clickedCategories="filteredCategories" />
  <ArticlesGrid :articles="filteredArticles" :state="state" />
</template>


  