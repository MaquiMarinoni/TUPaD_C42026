import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import type { Producto } from '@/features/products';

export interface CartItem {
  producto: Producto;
  cantidad: number;
}

interface CartState {
  items: CartItem[];
  add: (producto: Producto) => void;
  changeQuantity: (id: number, cantidad: number) => void;
  remove: (id: number) => void;
  clear: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set) => ({
      items: [],

      add: (producto) =>
        set((state) => {
          if (!producto.activo || !producto.disponible || producto.stock < 1) {
            return state;
          }

          const existing = state.items.find(
            (item) => item.producto.id === producto.id
          );

          if (existing) {
            return {
              items: state.items.map((item) =>
                item.producto.id === producto.id
                  ? {
                      ...item,
                      producto,
                      cantidad: Math.min(
                        item.cantidad + 1,
                        producto.stock
                      ),
                    }
                  : item
              ),
            };
          }

          return {
            items: [...state.items, { producto, cantidad: 1 }],
          };
        }),

      changeQuantity: (id, cantidad) =>
        set((state) => ({
          items: state.items
            .map((item) =>
              item.producto.id === id
                ? {
                    ...item,
                    cantidad: Math.max(
                      1,
                      Math.min(
                        Math.floor(cantidad || 1),
                        item.producto.stock
                      )
                    ),
                  }
                : item
            )
            .filter((item) => item.producto.stock > 0),
        })),

      remove: (id) =>
        set((state) => ({
          items: state.items.filter(
            (item) => item.producto.id !== id
          ),
        })),

      clear: () => set({ items: [] }),
    }),
    {
      name: 'foodstore-cart',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        items: state.items,
      }),
    }
  )
);
