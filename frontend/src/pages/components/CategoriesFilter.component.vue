<script setup lang="ts">
// import ArticleTag from './small/ArticleTag.small.vue'
import { fetchTagsList } from '../../services/api.service.ts'
import { fetchCategoryList } from '../../services/api.service.ts'
import ArticleCategory from './small/ArticleCategory.small .vue'
import { onMounted, ref } from 'vue';

const tags = ref<string[][]>([]);
const categories = ref<string[][]>([]);

// Split tags by groups of 4 to display 4 per row
const splitTags = (tags: string[]) => {
    const result: string[][] = [];
    for (let i = 0; i < tags.length; i += 4) {
        result.push(tags.slice(i, i + 4));
    }
    return result;
};

// Same thing for categories
const splitCategories = (categories: string[]) => {
    const result: string[][] = [];
    for (let i = 0; i < categories.length; i += 4) {
        result.push(categories.slice(i, i + 4));
    }
    return result;
};


onMounted(async () => {
    const fetchedTags = await fetchTagsList();
    const fetchedCategories = await fetchCategoryList();
    fetchedCategories.unshift("ALL");
    tags.value = splitTags(fetchedTags);
    categories.value = splitCategories(fetchedCategories);

});

defineProps<{ clickedCategories: string[] }>()
// Define the emits list, here when a category is clicked
defineEmits(["categoryClicked"]);

</script>


<template>
    <ul v-for="categoriesList in categories" :key="categoriesList[0]"
        class="list-inline list-unstyled d-flex justify-content-center pt-3 category-list">
        <div v-for="category in categoriesList">
            <ArticleCategory :category="category" :class="{ active: clickedCategories.includes(category) }" class="category" @click="$emit('categoryClicked', category);" />
        </div>
    </ul>
</template>

<style scoped>
.category-list {
    margin: 0;
    padding: 0;

}

.category {
    font-size: 0.9em;
}

@media (max-width: 768px) {

    .category {
        font-size: 0.65em;
    }
}
</style>