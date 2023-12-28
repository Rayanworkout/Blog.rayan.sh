<script setup lang="ts">
import MyHeader from './components/Header.component.vue'
import ArticlesGrid from './components/ArticlesGrid.component.vue'
import SearchInput from './components/SearchInput.component.vue'
import CategoriesFilter from './components/CategoriesFilter.component.vue'


import { onMounted, reactive, ref } from 'vue'
import { ArticleInGridType } from '../types/article.type.ts'
import axios from 'axios';

const articles = ref<ArticleInGridType[]>([])

const filteredArticles = ref<ArticleInGridType[]>([])
const categories = ref<string[]>([]);

const state = reactive({
    loading: true,
    error: false
})

onMounted(async () => {

    try {

        const data = await axios.get('http://127.0.0.1:8000/api/v1/articles/', {
      headers: {
        'Content-Type': 'application/json',
      }
    });
        if (data === null) {
            state.loading = false
            state.error = true
            throw new Error("No data returned from API.")
        }
        else {
            articles.value = data.data;
            state.loading = false
        }


    } catch (err: any) {
        state.loading = false
        state.error = true
        throw new Error(err)
    }
});


const filterArticles = () => {
    // I filter articles based on the categories clicked
    // If no categories are clicked, I return all articles
    if (categories.value.length === 0) {
      filteredArticles.value = articles.value;
    }
    // I filter articles based on the categories clicked
    // If no categories are clicked, I return all articles
    filteredArticles.value = articles.value.filter((article) => {
        return categories.value.includes(article.category);
    });
}


const handleCategoryClicked = (category: string) => {
    // I get the categories clicked with this event handler
    // Then I filter articles and I pass them as props
    if (category === "ALL") {
        categories.value = [];
        return;
    } else if (categories.value.includes(category)) {
        // If click on a category that is already clicked, remove it from the list
        // By filtering the array and keeping only the categories that are not the one clicked
        categories.value = categories.value.filter((category) => category !== category);
        return;
    }
    // Using spread operator to add the new category to the list
    // Instead of using push() which is not reactive and would not trigger a re-render (watcher)
    categories.value = [...categories.value, category];

    console.log(categories.value)
    filterArticles();
}

</script>

<template>
  <MyHeader />
  <SearchInput />
  <CategoriesFilter @categoryClicked="handleCategoryClicked" />
  <ArticlesGrid :articles="filteredArticles" :state="state" />
</template>


  