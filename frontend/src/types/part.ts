export interface Part {
    id: number;
    name: string;
    price: number | null;
    quantity: number;
    parent_id: number | null;
    total_price?: number;
    children: Part[];
}