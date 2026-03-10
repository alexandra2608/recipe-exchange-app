import { ref } from 'vue';
import axios from 'axios';

export function useRecipeUtils() {
  const getCurrentUserId = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return null;

      const response = await axios.get('http://localhost:8000/auth/users/me/', {
        headers: { Authorization: `Token ${token}` },
      });
      return response.data.id;
    } catch (error) {
      console.error('Ошибка при получении данных о пользователе:', error);
      return null;
    }
  };

  const fetchRecipeById = async (id) => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Ошибка при загрузке рецепта:', error);
      return null;
    }
  };


  return {
    getCurrentUserId,
    fetchRecipeById,
  };
}
