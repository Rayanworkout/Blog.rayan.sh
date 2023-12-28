

<script setup lang="ts">
import { ref } from 'vue'

import { debounceInput } from '../../services/debouncing.service.ts'


const searchInput = ref('')

const handleInput = () => {
    debounceInput(searchInput.value, test);
}

const test = () => {
    console.log('test')
}


</script>



<template>
    <div class="container">
        <div class="text-center">
            <input type="text" placeholder="Search" @input="handleInput" v-model="searchInput">
        </div>
    </div>
</template>
  


<style scoped>
input {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
    width: 15%;
    max-width: 500px;
}

@media (max-width: 768px) {
    input {
        width: 50%;
    }

}
</style>