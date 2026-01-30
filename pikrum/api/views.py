from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .services import process_new_image_upload, search_by_text, search_by_image
from .serializers import CatalogedImageSerializer

class CatalogUploadView(APIView):
    """Carica foto complesse e le scompone in oggetti (Detections)"""
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image_file = request.data.get('image_file')
        if not image_file:
            return Response({"error": "Nessun file caricato"}, status=status.HTTP_400_BAD_REQUEST)

        # Usiamo il servizio dedicato al Catalogo
        main_image = process_new_image_upload(image_file, is_reference_upload=False)
        
        # Restituiamo i dati dell'immagine madre tramite il serializer
        serializer = CatalogedImageSerializer(main_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReferenceUploadView(APIView):
    """Carica un prodotto singolo come termine di paragone (Reference)"""
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image_file = request.data.get('image_file')
        if not image_file:
            return Response({"error": "Nessun file caricato"}, status=status.HTTP_400_BAD_REQUEST)

        # Usiamo il servizio dedicato alla Reference
        ref_image = process_new_image_upload(image_file, is_reference_upload=True)
        
        serializer = CatalogedImageSerializer(ref_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SemanticSearchView(APIView):
    """Cerca nel catalogo via testo o caricando una foto di riferimento"""
    def post(self, request):
        query_text = request.data.get('query_text')
        query_image = request.data.get('query_image')

        if query_image:
            results = search_by_image(query_image)
        elif query_text:
            results = search_by_text(query_text)
        else:
            return Response({"error": "Invia query_text o query_image"}, status=status.HTTP_400_BAD_REQUEST)

        # Formattiamo i risultati per il frontend
        output = []
        for res in results:
            output.append({
                "id": res.id,
                "label": res.label,
                "distance": res.distance, # Quanto è simile? (0 è identico)
                "box": res.bounding_box,
                "image_url": res.parent_image.image_file.url,
                "tags": res.generated_tags
            })
        
        return Response(output, status=status.HTTP_200_OK)