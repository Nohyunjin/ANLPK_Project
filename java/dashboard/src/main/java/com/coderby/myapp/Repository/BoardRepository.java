package com.coderby.myapp.Repository;

import static com.mongodb.client.model.Sorts.ascending;
import static com.mongodb.client.model.Sorts.descending;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.bson.Document;
import org.springframework.stereotype.Repository;

import com.mongodb.client.AggregateIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Accumulators;
import com.mongodb.client.model.Aggregates;

@Repository
public class BoardRepository implements IBoardRepository {

	String conn = "mongodb://localhost:27017";

	MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");
	MongoDatabase db = mongoClient.getDatabase("news");
	MongoCollection<org.bson.Document> col = db.getCollection("news");

	@Override
	public long totalData() {
		System.out.println("repository ==================");
		long totalData = col.estimatedDocumentCount();

		System.out.println(totalData);

		return totalData;
	}

	@Override
	public Document dateRange() {

		AggregateIterable<Document> date = col.aggregate(Arrays.asList(
				Aggregates.group("", Accumulators.min("min", "$date"), Accumulators.max("max", "$date"))));

		MongoCursor<Document> cursor = date.cursor();

		Document doc = new Document();
		while (cursor.hasNext()) {
			doc = cursor.next();
			System.out.println(doc.getString("min"));
			System.out.println(doc.getString("max"));
		}

		return doc;
	}

	@Override
	public Map<String, Object> category() {

		AggregateIterable<Document> cate = col.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)),
				Aggregates.sort(descending("count"))));

		MongoCursor<Document> cursor = cate.cursor();

		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();

		List<String> label = new ArrayList<String>();
		List<Integer> count = new ArrayList<Integer>();

		while (cursor.hasNext()) {
			doc = cursor.next();
			label.add(doc.getString("_id"));
			count.add(doc.getInteger("count"));
		}
		map.put("label", label);
		map.put("count", count);
		System.out.println(map);

		return map;
	}

	@Override
	public List<String> weekCount() {
		AggregateIterable<Document> weekCount = col.aggregate(Arrays.asList(
				Aggregates.group("$week", Accumulators.sum("count", 1)),
				Aggregates.sort(ascending("_id"))));

		MongoCursor<Document> cursor = weekCount.cursor();

		Document doc = new Document();

		List<String> week = new ArrayList<String>();

		while (cursor.hasNext()) {
			doc = cursor.next();
			week.add(doc.toJson());
		}

		return week;
	}

	public Map<String, Object> freq() {
		AggregateIterable<Document> cate = col.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)),
				Aggregates.sort(descending("count"))));
		
		AggregateIterable<Document> source = col.aggregate(Arrays.asList(
				Aggregates.group("$source", Accumulators.sum("count", 1)),
				Aggregates.sort(descending("count"))));

		MongoCursor<Document> cursor = cate.cursor();
		MongoCursor<Document> cursor2 = source.cursor();

		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();

		List<String> cateTop = new ArrayList<String>();
		List<String> sourceTop = new ArrayList<String>();

		while (cursor.hasNext()) {
			doc = cursor.next();
			cateTop.add(doc.getString("_id"));
			break;
		}
		
		while (cursor2.hasNext()) {
			doc = cursor2.next();
			sourceTop.add(doc.getString("_id"));
			break;
		}
		map.put("cate", cateTop);
		map.put("source", sourceTop);

		return map;
	}

}