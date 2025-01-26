/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package main;
import com.fazecast.jSerialComm.*;
/**
 *
 * @author koalium
 */
public class formMain {
	
	public static void main(String args[]) {
		/* Set the Nimbus look and feel */
		//<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
		/* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
		 */
		
		//</editor-fold>
		//</editor-fold>
		java.awt.EventQueue.invokeLater(new Runnable() {
			
			public void run() {
			
				
				//forming = new Forming();
		               // forming.setVisible(true);
				frm = new Formium();
				frm.setVisible(true);
				
			}

			
		});
		
	}
	

	//
	//
	
	private static Formium frm;
	
}
