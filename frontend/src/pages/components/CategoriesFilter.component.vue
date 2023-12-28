<script setup lang="ts">
import axios from 'axios';
// import ArticleTag from './small/ArticleTag.small.vue'
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

const getTagsOrCategoriesList = async (element: "tags" | "categories") => {

    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/${element}/`, {
            headers: {
                'Content-Type': 'application/json',
            }
        })

        return response.data;

    } catch (error: any) {
        return null;
    }
};

onMounted(async () => {
    const fetchedTags = await getTagsOrCategoriesList("tags");
    const fetchedCategories = await getTagsOrCategoriesList("categories");
    fetchedCategories.unshift("ALL");
    tags.value = splitTags(fetchedTags);
    categories.value = splitCategories(fetchedCategories);


});

// const clickedCategories = ref<string[]>([]);

// const handleClick = (e: any) => {
//     // <i class="bi bi-check"></i>
//     // I empty the array if the user clicks on the "ALL" category
//     if (e.target.innerText === "ALL") {
//         clickedCategories.value = [];
//         return;
//     } else if (clickedCategories.value.includes(e.target.innerText)) {
//         // If click on a category that is already clicked, remove it from the list
//         // By filtering the array and keeping only the categories that are not the one clicked
//         clickedCategories.value = clickedCategories.value.filter((category) => category !== e.target.innerText);
//         return;
//     }
//     // Using spread operator to add the new category to the list
//     // Instead of using push() which is not reactive and would not trigger a re-render (watcher)
//     clickedCategories.value = [...clickedCategories.value, e.target.innerText];

// }


</script>


<template>
    <ul v-for="categoryList in categories" :key="categoryList[0]"
        class="list-inline list-unstyled d-flex justify-content-center pt-3 category-list">
        <div v-for="category in categoryList">
            <ArticleCategory :category="category" class="category" @click="$emit('categoryClicked', category)" />
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