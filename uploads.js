const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://pghedmdfnbjyxzryogcl.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBnaGVkbWRmbmJqeXh6cnlvZ2NsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMzMTU2MTksImV4cCI6MjAyODg5MTYxOX0.VTkdE7EeykOBPqdKBbP3DAHAKahqOd_KeyepHE1ffqw';
const supabase = createClient(supabaseUrl, supabaseKey);

async function processJson(filename) {
    try {
      const data = fs.readFileSync(filename, 'utf8');
      const jsonData = JSON.parse(data);
  
      for (const product of jsonData) {
        const almacen = product.Almacen;
        const nombre = product.Nombre;
        const precioOriginal = parseFloat(product['Precio original']);
        const precioDescuento = parseFloat(product['Precio descuento']);
        const fecha = product.Fecha;
        const precio = isNaN(precioOriginal) || isNaN(precioDescuento) ? null : Math.min(precioOriginal, precioDescuento);
  
        // Check if almacen exists and insert if not
        let { data: almacenData, error: almacenError } = await supabase
          .from('almacenes')
          .select('almacen_id')
          .eq('nombre', almacen)
          .maybeSingle();
  
        if (!almacenData && !almacenError) {
          const { data: newAlmacenData, error: newAlmacenError } = await supabase
            .from('almacenes')
            .insert([{ nombre: almacen, ubicacion: null }])
            .single();
          almacenData = newAlmacenData;
          if (newAlmacenError) console.error('Error inserting new almacen:', newAlmacenError);
        }
  
        // Check if producto exists and insert if not
        let { data: productoData, error: productoError } = await supabase
          .from('productos')
          .select('producto_id')
          .eq('nombre', nombre)
          .maybeSingle();
  
        if (!productoData && !productoError) {
          const { data: newProductoData, error: newProductoError } = await supabase
            .from('productos')
            .insert([{ nombre: nombre, calificacion: null }])
            .single();
          productoData = newProductoData;
          if (newProductoError) console.error('Error inserting new producto:', newProductoError);
        } else if (productoError) {
          console.error('Error retrieving producto:', productoError);
        }
  
        // Now that productoData is retrieved correctly, proceed with inserts
        if (almacenData && productoData) {
          await supabase
            .from('producto_almacen')
            .insert([{ producto_id: productoData.producto_id, almacen_id: almacenData.almacen_id, stock: null }]);
  
          await supabase
            .from('precio_producto')
            .insert([{ producto_id: productoData.producto_id, almacen_id: almacenData.almacen_id, precio: precio, fecha: fecha }]);
        } else {
          console.error('Failed to retrieve or create almacen or producto');
        }
      }
    } catch (err) {
      console.error('Error processing JSON:', err);
    }
  }
  

processJson('alkosto_productos.json');

processJson('carulla_productos.json');

processJson('olimpica_productos.json');