package com.coderby.myapp.Controller;

import java.util.List;
import java.util.Map;

import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.coderby.myapp.Service.IBoardService;

@Controller
public class BoardController {

	@Autowired
	IBoardService boardService;

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Model model) {
		
		System.out.println("controller ===========");
		
		// 총 기사 개수 
		long totalData = boardService.totalData();		
		model.addAttribute("totalData", totalData);
		
		// 데이터 수집 기간 
		Document dateRange = boardService.dateRange();
		model.addAttribute("min", dateRange.get("min"));
		model.addAttribute("max", dateRange.get("max"));
		
		// 카테고리, 언론사 빈도수 TOP1
		Map<String, Object> freq = boardService.freq();
		model.addAttribute("freq", freq);
		
		
		// 카테고리별 분포 
		Map<String, Object> map = boardService.category();
		model.addAttribute("map", map);
		
		// 기사 수집 추이 
		List<String> week = boardService.weekCount();
		model.addAttribute("weekCount", week);
		
		return "index";
	}

	
}