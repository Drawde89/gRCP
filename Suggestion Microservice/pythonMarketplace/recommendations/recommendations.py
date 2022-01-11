from concurrent import futures #the needed thread pool for grpc
import random
import grpc
import recommendations_pb2_grpc
from recommendations_pb2 import(
    SCIENCE_FICTION,
    SELF_HELP,
    BookCategory,
    BookRecommendation,
    RecommendationResponse
)

#Dict/Map of books by category where the key is the genre enum and a list of books is the value

books_by_category = {

    BookCategory.MYSTERY: [
        BookRecommendation(id = 1, title="The Maltese Falcon"),
        BookRecommendation(id = 2, title="Murder On The Orient Express"),
        BookRecommendation(id = 3, title="The Hounds of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
         BookRecommendation(id = 4, title="The Hitchiker's Guide to the Galaxy"),
         BookRecommendation(id = 5, title="Ender's Game"),
         BookRecommendation(id = 6, title="The Dune Chronicles"),
     ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id = 7, title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id = 8, title="How to Win Friends and Influence People"),
        BookRecommendation(id = 9, title="Man's Search for Meaning"),
      ]


}

#implementation of a microservice
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    #this class must have the same name as the rpc defined in the protobuf file
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            #ends the request and sets the status code to NOT_FOUND
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        #retrieves the list of books
        books_for_category = books_by_category[request.category]
        #limits the number of max_results to ensure we are not trying to access a part of the list that doesnt exist
        num_results = min(request.max_results, len(books_for_category))
        #returns a random sample from the list and num_results is the max that can be chosen
        books_to_recommend = random.sample(books_for_category, num_results)

        #uses repeated BookRecommendation recommendations from the protobuf file to send the response
        return RecommendationResponse(recommendations = books_to_recommend)



def serve():
    print("Server is Running")
    #creats a grpc server that uses 10 threads 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #associating the calss with the server
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    #tells the server to run on port 50051
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    
    

