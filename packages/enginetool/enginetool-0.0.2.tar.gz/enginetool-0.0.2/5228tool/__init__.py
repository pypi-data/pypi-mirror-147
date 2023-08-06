import numpy
import matplotlib.pyplot as plt
import csv

class Engine:
	def __init__(self, bore, stroke, CR, ncyl):
		"""
		Creates an Engine object. Defines the bore, stroke, compression ratio, and number of cylinders of the given engine
		"""
		
		self.bore = bore
		self.stroke = stroke
		self.CR = CR
		self.ncyl = ncyl


	def volvsCA(self,sheet = False):
		"""
		Does a sweep of engine volume versus crank angle. 
		Input argument sheet is the name of the .csv file that will be written to (optional)

		Returns a table of crank angle, sealed volume, and volume. Also creates a graph of sealed volume vs crank angle
		If a sheet is given as an input argument, there is no output to the console and instead creates a file "sheet_name.csv" containg the values
		"""

		vd = (numpy.pi/4)*(self.bore*self.bore*self.stroke*0.000001)
		vc = vd /(self.CR-1)
		size = 360
		vvc = [None]*size
		vol = [None]*size
		i = 0

		print("Deg","V/Vc","Volume", sep ="\t")		
		for d in range(-180,180):
			vvc[i] = 1+0.5*(self.CR-1)*(self.CR+1-numpy.cos(numpy.radians(d))-numpy.sqrt(self.CR*self.CR-numpy.sin(numpy.radians(d))*numpy.sin(numpy.radians(d))))
			vol[i] = vvc[i]/self.CR
			print(d,vvc[i],vol[i], sep = "\t")
			i = i+1

		x = range(-180,180)
		

		if sheet != False:
			try:
				header = ['Crank Angle', 'Sealed Volume (V/Vc)','Volume']
				with open(sheet,'w',newline = '') as f:
					writer = csv.writer(f, dialect = 'excel')

					writer.writerow(header)

					for i in x:
						writer.writerow([x[i], vvc[i],vol[i]])
			except:
				print("Error has occured accessing spreadsheet")

		else:
			plt.plot(x,vvc)
			plt.ylabel("Sealed Volume (V/Vc)")
			plt.xlabel("Crank Angle (deg)")
			plt.title("Volume vs Crank Angle")
			plt.show()

	def wiebe(self,thetaS,thetaD,a,n,sheet = False):
		"""
		Defines the Wiebe function and its derivative (NAHR and NAHRR) based on inputs.
		Inputs:
			thetaS: start of burn in degrees
			thetaD: duration of burn in degrees
			a and n: constants associated with Wiebe function
			sheet: name of .csv results will be written to

		Returns a table of crank angle, Wiebe function values, and dXb/dTheta values. Also creates a graph of heat release versus crank angle
		If a sheet is given as an input argument, there is no output to the console and instead creates a file "sheet_name.csv" containg the value
		"""

		size = 360
		wiebe = [0]*size
		dxb = [0]*size
		i=0

		print("Deg","Wiebe","dxb", sep = "\t")
		for d in range(-180,180):
			if d<thetaS:
				wiebe[i] = 0
				dxb[i] = 0
				i = i+1
				print(d, wiebe[i], dxb[i],sep = "\t")
			else:
				temp = -a*((d-thetaS)/thetaD)**float(n)
				wiebe[i] = 1-numpy.exp(temp)
				dxb[i] = 10*(wiebe[i]-wiebe[i-1])
				print(d, wiebe[i], dxb[i],sep = "\t")
				i = i+1

		x = range(-180,180)

		if sheet != False:
			try:
				header = ['Crank Angle', 'Wiebe Function','dXb/dTheta']
				with open(sheet,'w', newline = '') as f:
					writer = csv.writer(f, dialect = 'excel')

					writer.writerow(header)

					for i in x:
						writer.writerow([x[i], wiebe[i],dxb[i]])
			except:
				print("Error has occured accessing spreadsheet")

		else:
			plt.plot(x,wiebe, label = "Wiebe Function")
			plt.plot(x,dxb, label = "dXb/dTheta")
			plt.xlabel("Crank Angle (deg)")
			plt.ylabel("NAHRR")
			plt.xlim(-30,70)
			plt.title("Heat Release vs CA")
			plt.show()

	def RFD(self,Nrpm,Wb, Eta, QLHV, AFRs, lamb, ev, Tim, Rim,sheet = False):
		"""
		Mimics the RFD Excel tool and outputs all the same values

		Inputs:
			Nrpm: RPM of the engine 
			Wb: Brake power
			Eta: Engine efficiency (decimal form)
			QLHV: Lower heating value of the fuel
			AFRs: Stoichiometric air-fuel ratio
			lamb: lambda or the excess air ratio
			ev: Volumetric efficiency
			Tim: Intake manifold temperature
			Rim: Intake manifold gas constant
			sheet: name of .csv results will be written to

		Outputs:
			Engine displacement
			Total volume
			Brake Mean Effective Power (BMEP)
			Engine Torque
			Fuel mass-flow rate
			Air mass-flow rate
			Total intake mass-flow rate
			Intake manifold pressure

		Returns all these values as a list in the console.
		If a sheet is given as an input argument, there is no output to the console and instead creates a file "sheet_name.csv" containg the values
		"""

		vd = (numpy.pi/4)*(self.bore*self.bore*self.stroke*0.000000001)
		eng_disp = vd
		v_tot = eng_disp*self.ncyl
		BMEP = 2*Wb/(100*v_tot*Nrpm/60)
		eng_torq = Wb*1000/(2*numpy.pi*Nrpm/60)
		m_f = Wb/(Eta*QLHV*1000)
		m_a = lamb*AFRs*m_f
		m_tot = m_f+m_a
		pim = (2/(Nrpm/60))*((Rim*Tim)/(ev*v_tot))*(1/(AFRs*lamb)+1)*m_a
		pim = pim/(10**5)


		if sheet != False:
			try:
				with open(sheet,'w', newline = '') as f:
					writer = csv.writer(f, dialect = 'excel')

					writer.writerow(["Engine Displacement (m^3) ",eng_disp])
					writer.writerow(["V total (m^3) ",v_tot])
					writer.writerow(["BMEP (bar) ", BMEP])
					writer.writerow(["Engine Torque (Nm) ",eng_torq])
					writer.writerow(["Fuel Mass Flow Rate (kg/sec) ", m_f])
					writer.writerow(["Air Mass Flow Rate (kg/sec) ", m_a])
					writer.writerow(["Intake Total Mass Flow Rate (kg/sec) ", m_tot])
					writer.writerow(["Intake Manifold Pressure (bar) ", pim])
			except:
				print("Error has occured accessing spreadsheet")

		else:
			print("Engine Displacement (m^3) \t",eng_disp)
			print("V total (m^3) \t",v_tot)
			print("BMEP (bar) \t", BMEP)
			print("Engine Torque (Nm) \t",eng_torq)
			print("Fuel Mass Flow Rate (kg/sec) \t", m_f)
			print("Air Mass Flow Rate (kg/sec) \t", m_a)
			print("Intake Total Mass Flow Rate (kg/sec) \t", m_tot)
			print("Intake Manifold Pressure (bar) \t", pim)





e = Engine(119,175,13,6)
e.RFD(1300,253,0.4,49.85703,17.056,1,1.53242,319.37,299.8563,'poop.csv')




