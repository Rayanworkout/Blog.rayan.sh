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
  allCategories.value.unshift("ALL");

  // I use setTimeout to wait for the articles to be fetched
  setTimeout(() => {
    // Initialize filtered articles with all articles
    filteredArticles.value = articles.value;
  }, 200);

});

// category: string,

// filteredCategories: Ref<string[]>,

// articles: Ref<ArticleInGridType[]>,

// filteredArticles: Ref<ArticleInGridType[]>) => {


// Apply filtering with the imported function
const applyFiltering = (category: string) => {
  handleCategoryClicked(category, filteredCategories, articles, filteredArticles);
}

</script>

<template>
  <MyHeader />
  <SearchInput />
  <CategoriesFilter @categoryClicked="applyFiltering" :clickedCategories="filteredCategories" />
  <ArticlesGrid :articles="filteredArticles" :state="state" />
</template>


  