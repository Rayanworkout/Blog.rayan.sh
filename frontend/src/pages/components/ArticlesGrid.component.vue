<script setup lang="ts">
import ArticleInGrid from './ArticleInGrid.component.vue'
import { onMounted, reactive, ref } from 'vue'
import { ArticleInGridType } from '../../types/article.type.ts'
import axios from 'axios';

const articles = ref<ArticleInGridType[]>([])

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

</script>

<template>
    <div class="container py-4">
        <div v-if="state.loading" class="text-center">Loading <span class="cursor">_</span></div>
        <div v-if="state.error" class="text-center">Error while fetching the articles ...</div>
        <div v-if="articles.length === 0" class="text-center">Nothing here for the moment ...</div>
        <div v-else>
            <TransitionGroup name="fade">
                <div v-for="article in articles" :key="article.id">
                    <ArticleInGrid :article="article" />
                </div>
            </TransitionGroup>
        </div>
    </div>
</template>