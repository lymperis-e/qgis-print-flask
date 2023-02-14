import React from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { useState } from 'react';
import { EditControl } from 'react-leaflet-draw';

import axios from 'axios';

import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'

const MyMap = () => {
    const [bounds, setBounds] = useState(null);
    const [title, setTitle] = useState("");

    const handleDrawCreated = (e) => {
        const type = e.layerType;
        const layer = e.layer;
        if (type === 'rectangle') {

            let layerBounds = layer.getBounds()
            setBounds({
                xmin: layerBounds._southWest.lng,
                ymin: layerBounds._southWest.lat,
                xmax: layerBounds._northEast.lng,
                ymax: layerBounds._northEast.lat,
            })
        }
    }

    const handleTitleChange = (e)=>{
        setTitle(event.target.value);
    }


    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/coordinates', { xmin: bounds.xmin, xmax: bounds.xmax, ymin: bounds.ymin, ymax: bounds.ymax, title:title }, {
                responseType: 'blob'
            });
            console.log(response);

            // Hack to get the response file
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'myFile.pdf')
            document.body.appendChild(link)
            link.click()

        } catch (error) {
            console.error(error);
        }
    };

    return (
        <MapContainer center={[51.505, -0.09]} zoom={13} style={{ "height": "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            <FeatureGroup>
                <EditControl
                    position='topright'
                    onCreated={handleDrawCreated}
                    draw={{

                        rectangle: { showArea: false }, // disable showArea
                    }}
                />
            </FeatureGroup>

            <button onClick={handleSubmit} style={{ "position": "absolute", "zIndex": "1000" }}>Submit</button>

            <label>
                Title:
                <input type="text" value={title} onChange={handleTitleChange} />
            </label>

        </MapContainer >
    );
};

export default MyMap;