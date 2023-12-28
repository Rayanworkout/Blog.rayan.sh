<script setup lang="ts">
import MyHeader from './components/Header.component.vue'
import ArticlesGrid from './components/ArticlesGrid.component.vue'
import SearchInput from './components/SearchInput.component.vue'
import CategoriesFilter from './components/CategoriesFilter.component.vue'
import { fetchArticles, fetchCategoryList } from '../services/api.service.ts'

import { onMounted, reactive, ref } from 'vue'
import { ArticleInGridType } from '../types/article.type.ts'

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

  // Initialize filtered articles with all articles
  filteredArticles.value = articles.value;

});

const filterArticles = (filteredCategories: string[]) => {
  // I filter articles based on the categories clicked
  filteredArticles.value = articles.value.filter((article) => {
    // Check if the article's category is included in the filtered categories array
    return filteredCategories.includes(article.category);
  });
}


const handleCategoryClicked = (category: string) => {
  // The category prop passed is the category clicked as string


  // I get the categories clicked with this event handler
  // Then I filter articles and I pass them as props
  if (category === "ALL") {
    // If click on "ALL" category, I reset the list of clicked categories
    // And I return all articles
    filteredCategories.value = [];
    filteredArticles.value = articles.value;
    return;


    // If the clicked category is already in the list of clicked categories
  } else if (filteredCategories.value.includes(category)) {
    // I remove this category from the list
    filteredCategories.value = filteredCategories.value.filter((cat) => cat !== category);

  } else {
    // Using spread operator to add the new category to the list
    // Instead of using push() which is not reactive and would not trigger a re-render (watcher)
    filteredCategories.value = [...filteredCategories.value, category];
  }


  // And finally I filter articles
  filterArticles(filteredCategories.value);

}

</script>

<template>
  <MyHeader />
  <SearchInput />
  <CategoriesFilter @categoryClicked="handleCategoryClicked" :clickedCategories="filteredCategories"/>
  <ArticlesGrid :articles="filteredArticles" :state="state" />
</template>


  