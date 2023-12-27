<script setup lang="ts">
import ArticleInGrid from './ArticleInGrid.component.vue'
import api from '../../services/api.ts'
import { onMounted, reactive, ref } from 'vue'
import { ArticleInGridType } from '../../types/article.type.ts'

const articles = ref<ArticleInGridType[]>([])

const state = reactive({
    loading: true,
})

onMounted(async () => {
    const response = await api.getArticlesList();
    articles.value = response;
    state.loading = false
})

</script>

<template>
    <div class="container py-4">
        <div v-if="state.loading" class="text-center">Loading ...</div>
        <TransitionGroup name="fade">
            <div v-if="!state.loading">
                <div v-for="article in articles" :key="article.id">
                    <ArticleInGrid :article="article" />
                </div>
            </div>
        </TransitionGroup>
    </div>
</template>