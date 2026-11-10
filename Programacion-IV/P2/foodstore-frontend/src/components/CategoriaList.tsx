import React from 'react';
import { flexRender, type Table } from '@tanstack/react-table';
import { ArrowDown, ArrowUp, ArrowUpDown, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import type { Categoria } from '../types/categoria';

interface CategoriaListProps {
  table: Table<Categoria>;
  globalFilter: string;
  onGlobalFilterChange: (value: string) => void;
}

export const CategoriaList: React.FC<CategoriaListProps> = ({
  table,
  globalFilter,
  onGlobalFilterChange,
}) => {
  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={globalFilter ?? ''}
            onChange={(e) => onGlobalFilterChange(e.target.value)}
            placeholder="Filtrar categorías por nombre o descripción..."
            className="w-full rounded-lg border border-slate-300 pl-9 pr-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
        </div>
        <span className="text-xs font-medium text-slate-500">
          Mostrando {table.getRowModel().rows.length} de {table.getFilteredRowModel().rows.length} registros
        </span>
      </div>

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    const canSort = header.column.getCanSort();
                    const sorted = header.column.getIsSorted();
                    return (
                      <th
                        key={header.id}
                        scope="col"
                        onClick={canSort ? header.column.getToggleSortingHandler() : undefined}
                        className={`px-6 py-3.5 text-left text-xs font-semibold uppercase tracking-wider text-slate-600 ${
                          canSort ? 'cursor-pointer select-none hover:bg-slate-100 transition-colors' : ''
                        }`}
                      >
                        <div className="flex items-center gap-1.5">
                          {header.isPlaceholder
                            ? null
                            : flexRender(header.column.columnDef.header, header.getContext())}
                          {canSort && (
                            <span className="text-slate-400">
                              {sorted === 'asc' ? (
                                <ArrowUp className="h-3.5 w-3.5 text-indigo-600" />
                              ) : sorted === 'desc' ? (
                                <ArrowDown className="h-3.5 w-3.5 text-indigo-600" />
                              ) : (
                                <ArrowUpDown className="h-3.5 w-3.5" />
                              )}
                            </span>
                          )}
                        </div>
                      </th>
                    );
                  })}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white">
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id} className="hover:bg-slate-50/80 transition-colors">
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-6 py-4 text-sm text-slate-700 whitespace-nowrap">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-6 py-3">
          <div className="text-xs font-medium text-slate-600">
            Página <span className="font-semibold text-slate-900">{table.getState().pagination.pageIndex + 1}</span> de{' '}
            <span className="font-semibold text-slate-900">{Math.max(1, table.getPageCount())}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
              className="inline-flex items-center gap-1 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
            >
              <ChevronLeft className="h-4 w-4" />
              Anterior
            </button>
            <button
              type="button"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
              className="inline-flex items-center gap-1 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
            >
              Siguiente
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
